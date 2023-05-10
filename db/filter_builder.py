from datetime import datetime
from sqlalchemy import or_, and_


class FilterBuilder:
    def __init__(self, model):
        self.model = model

    def build_filters(self, filters):
        filter_conditions = []

        for key, filter_options in filters.items():
            if filter_options and hasattr(self.model, key):
                column = getattr(self.model, key)
                operaton = filter_options.get('op', 'eq')
                value = filter_options.get('value')

                if operaton == 'is_null':
                    filter_conditions.append(column.is_(None))
                elif value == "<null>":
                    filter_conditions.append(column.is_(None))
                elif operaton == 'eq':
                    filter_conditions.append(column == value)
                elif operaton == 'ilike':
                    filter_conditions.append(column.ilike(value))
                elif operaton == 'gt':
                    if key in ['start_date', 'due_date', 'created_on', 'updated_on', 'closed_on']:
                        value = datetime.strptime(value, '%Y-%m-%d')
                    filter_conditions.append(column > value)
                elif operaton == 'lt':
                    filter_conditions.append(column < value)
                elif operaton == 'ge':
                    filter_conditions.append(column >= value)
                elif operaton == 'le':
                    filter_conditions.append(column <= value)
                elif operaton == 'or':
                    or_filters = value
                    or_conditions = [self.build_filters({key: or_filter}) for or_filter in or_filters]
                    filter_conditions.append(or_(*or_conditions))
                else:
                    raise ValueError(f"Invalid filter operator '{operaton}' for attribute '{key}'.")
            else:
                raise ValueError(f"Invalid filter attribute '{key}'.")

        return and_(True, *filter_conditions)
