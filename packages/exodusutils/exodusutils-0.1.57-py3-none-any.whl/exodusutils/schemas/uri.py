import os
import traceback
from io import BytesIO
from typing import List, Optional
from urllib.parse import urlparse

import pandas as pd
from minio.api import Minio
from pydantic import BaseModel
from urllib3.response import HTTPResponse

from exodusutils.exceptions.exceptions import ExodusForbidden


class MinioURI(BaseModel):
    """
    The Minio URI.
    """

    bucket: str
    key: str

    @property
    def url(self) -> str:
        """
        Returns `"s3a://{bucket}/{object}"`.
        """
        return f"s3a://{self.bucket}/{self.key}"

    @classmethod
    def parse(cls, s: str):
        """
        Parses a string to a Minio compatible URI. The scheme could be either `s3`, `s3a`, or `s3n`.

        Parameters
        ----------
        s : str
            The string to parse.
        """
        parsed = urlparse(s)
        if parsed.scheme not in ["s3", "s3a", "s3n"]:
            raise ExodusForbidden(f"Invalid scheme: {parsed.scheme}")
        return cls(bucket=parsed.netloc, key=parsed.path.lstrip("/"))

    def put_df(self, minio: Minio, df: pd.DataFrame):
        """
        Stores the given df in Minio and returns its URI

        Parameters
        minio : Minio
            The minio client
        df : pd.DataFrame
            The dataframe to store
        """
        csv_bytes = df.to_csv().encode("utf-8")
        csv_buffer = BytesIO(csv_bytes)
        if not minio.bucket_exists(self.bucket):
            minio.make_bucket(self.bucket)
        minio.put_object(self.bucket, self.key, csv_buffer, length=len(csv_bytes), content_type="application/csv")

    def get_df(self, minio: Minio, header: List[str]) -> Optional[pd.DataFrame]:
        """
        Returns a Pandas dataframe parsed from this Minio URI. Returns `None` on failure.

        Parameters
        ----------
        minio : Minio
            The Minio client.
        header : List[str]
            The header we want to parse the dataframe with.

        Returns
        -------
        Optional[pd.DataFrame]
            The parsed dataframe.

        """
        try:
            resp: HTTPResponse = minio.get_object(self.bucket, self.key)
            if not resp.data:
                # Should be inpossible
                raise ValueError
            return pd.DataFrame(pd.read_csv(BytesIO(resp.data), usecols=header))
        except Exception:
            traceback.print_exc()
