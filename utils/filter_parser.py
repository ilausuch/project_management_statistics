import json


class FilterParser:
    def add_filtering_arguments(self, parser):
        parser.add_argument('--filter-project', type=str, help='Filter by project')
        parser.add_argument('--filter-type', type=str, help='Filter by type')
        parser.add_argument('--filter-tags', type=str, help='Filter by tags')
        parser.add_argument('--filter-context', type=str, help='Filter by context')
        parser.add_argument('--filter-status', type=str, help='Filter by status')
        parser.add_argument('--filter-priority', type=str, help='Filter by priority')
        parser.add_argument('--filter-author', type=str, help='Filter by author')
        parser.add_argument('--filter-assigned_to', type=str, help='Filter by assigned_to')
        parser.add_argument('--filter-target_version', type=str, help='Filter by target_version')
        parser.add_argument('--filter', type=str, help='Filter by JSON string')

    def _parse_filters(self, args):
        filters = json.loads(args.filter) if args.filter else {}

        individual_filters = {
            'project': args.filter_project,
            'type': args.filter_type,
            'tags': args.filter_tags,
            'context': args.filter_context,
            'status': args.filter_status,
            'priority': args.filter_priority,
            'author': args.filter_author,
            'assigned_to': args.filter_assigned_to,
            'target_version': args.filter_target_version
        }

        for key, value in individual_filters.items():
            if value is not None:
                filters[key] = {'op': 'eq', 'value': value}

        for key, value in filters.items():
            if not isinstance(value, dict):
                filters[key] = {'op': 'eq', 'value': value}

        return filters

    def get_filters(self, args):
        return self._parse_filters(args)
