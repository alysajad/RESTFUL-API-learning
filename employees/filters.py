import django_filters
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):
    designation = django_filters.CharFilter(field_name='designation', lookup_expr='iexact')
    emp_name = django_filters.CharFilter(field_name='emp_name', lookup_expr='icontains')
    #id = django_filters.RangeFilter(field_name='id') #id from and to range filter
    id_min=django_filters.CharFilter(method='filter_by_id_range',label='from EMP ID')
    id_max=django_filters.CharFilter(method='filter_by_id_range',label='to EMP ID')

    #custom method for id range filter
    class Meta:
        model = Employee
        fields = ['designation', 'emp_name', 'id', 'id_min', 'id_max' ]

    #custom method for id range filter
    def filter_by_id_range(self, queryset, name, value):
      if name == 'id_min':
          return queryset.filter(id__gte=value)
      
      elif name == 'id_max':
          return queryset.filter(id__lte=value)
        #custom filtering example
        #https://django-filter.readthedocs.io/en/stable/ref/filters.html#custom-filtering