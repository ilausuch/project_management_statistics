from sqlalchemy import or_
from db.filter_builder import FilterBuilder
from db.models import Issue


def test_filter_builder():
    filter_builder = FilterBuilder(Issue)

    filters = {
        'project': {'op': 'eq', 'value': 'Project A'},
        'tags': {'op': 'ilike', 'value': '%tag1%'},
        'status': {
            'op': 'or',
            'value': [
                {'op': 'eq', 'value': 'New'},
                {'op': 'eq', 'value': 'In Progress'}
            ]
        },
        'start_date': {'op': 'gt', 'value': '2022-01-01'},
        'target_version': {'op': 'is_null'},
        'author': {'op': 'eq', 'value': '<null>'}
    }

    filter_conditions = filter_builder.build_filters(filters)

    expected_filters = (
        Issue.project == 'Project A',
        or_(Issue.status == 'New', Issue.status == 'In Progress'),
        Issue.tags.ilike('%tag1%'),
        Issue.start_date > '2022-01-01',
        Issue.target_version == None,  # pylint: disable=singleton-comparison
        Issue.author == None  # pylint: disable=singleton-comparison
    )

    filter_conditions_strs = set(map(lambda x: str(x).strip('()'), filter_conditions.clauses))
    expected_filters_strs = set(map(lambda x: str(x).strip('()'), expected_filters))

    assert filter_conditions_strs == expected_filters_strs
