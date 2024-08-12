"""
The use of pynamodb is optional, installing additional dependencies is sometimes redundant
    and in this case we could just use boto3 to work with the DynamoDB table.
But I added it to show that it is possible to use models when working with DynamoDB tables.

"""

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection


class WinnerOpponentIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index (GSI) for querying by 'winner' and 'opponent'.

    """

    class Meta:
        index_name = "winner_opponent_index"
        projection = AllProjection()

    winner = UnicodeAttribute(hash_key=True)
    opponent = UnicodeAttribute(range_key=True)


class WinnerTimestampIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index (GSI) for querying by 'winner' and 'timestamp'.

    """

    class Meta:
        index_name = "winner_timestamp_index"
        projection = AllProjection()

    winner = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True)


class BattleModel(Model):
    """
    Model 'Battle' for the DynamoDB table.

    """

    class Meta:
        table_name = "ede-demo-battle"

    # Table attributes
    id = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute()
    winner = UnicodeAttribute()
    opponent = UnicodeAttribute()
    winner_total_stats = NumberAttribute()
    opponent_total_stats = NumberAttribute()

    # GSIs
    winner_opponent_index = WinnerOpponentIndex()
    winner_timestamp_index = WinnerTimestampIndex()
