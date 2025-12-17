import pandas as pd
from sqlalchemy import create_engine, text
from .core.definitions import FeatureView

class KairosClient:
    def __init__(self, db_url="postgresql://admin:password@localhost:5432/kairos_core"):
        self.engine = create_engine(db_url)
        self.registry = {} # Simple in-memory registry for now

    def register_view(self, view: FeatureView):
        """Registers a Feature View definition."""
        self.registry[view.name] = view
        print(f"Registered Feature View: {view.name}")

    def get_historical_features(self, entity_df: pd.DataFrame, feature_refs: list) -> pd.DataFrame:
        """
        Retrieves point-in-time correct features.
        
        Args:
            entity_df: DataFrame containing [entity_id, event_timestamp]
            feature_refs: List of "view_name:feature_name" strings
        """
        # 1. Upload entity_df to a temp table
        entity_df.to_sql("temp_entity_lookup", self.engine, if_exists="replace", index=False)
        
        # 2. Construct the Point-in-Time SQL Query
        # This is the "Secret Sauce" of Feature Stores
        view_name = feature_refs[0].split(":")[0]
        view = self.registry.get(view_name)
        if not view:
            raise ValueError(f"Feature View {view_name} not found!")

        # We join the Entity Request with the Feature Data
        # Condition: Feature Timestamp <= Request Timestamp
        query = f"""
        SELECT 
            t.user_id,
            t.event_timestamp as request_time,
            f.event_timestamp as feature_time,
            f.amount,
            f.is_fraud
        FROM temp_entity_lookup t
        LEFT JOIN offline_store.transactions f
        ON t.user_id = f.user_id
        AND f.event_timestamp <= t.event_timestamp -- NO FUTURE LEAKAGE
        -- Get the most recent value relative to the request time
        WHERE f.event_timestamp = (
            SELECT MAX(event_timestamp)
            FROM offline_store.transactions f2
            WHERE f2.user_id = t.user_id
            AND f2.event_timestamp <= t.event_timestamp
        )
        """
        
        # 3. Execute and Return
        result = pd.read_sql(query, self.engine)
        return result