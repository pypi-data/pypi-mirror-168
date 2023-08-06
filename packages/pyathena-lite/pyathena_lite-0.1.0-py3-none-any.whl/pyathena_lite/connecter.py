from pyathena import connect


class AthenaConnecter:
    def __init__(self, staging_dir: str, region: str) -> None:
        """
        Args:
            staging_dir - AWS s3 path
            region - AWS region
        """
        self.cursor = connect(s3_staging_dir=staging_dir,
                 region_name=region).cursor()
    
    def execute(self, query:str) -> None:
        return self.cursor.execute(query)