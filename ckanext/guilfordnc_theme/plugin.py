import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def recent_datasets(num=5):
    """Return a list of recent datasets."""
    sorted_datasets = []
    datasets = toolkit.get_action('current_package_list_with_resources')({},{'limit': num})
    if datasets:
        sorted_datasets = sorted(datasets, key=lambda k: k['metadata_modified'], reverse=True)
    return sorted_datasets[:num]


def popular_datasets(num=5):
    """Return a list of popular datasets."""
    datasets = []
    search = toolkit.get_action('package_search')({},{'rows': num, 'sort': 'views_recent desc'})
    if search.get('results'):
        datasets = search.get('results')
    return datasets[:num]


def dataset_count():
    """Return a count of all datasets"""
    count = 0
    result = toolkit.get_action('package_search')({}, {'rows': 1})
    if result.get('count'):
        count = result.get('count')
    return count


def groups(num=12):
    """Return a list of groups"""
    groups = toolkit.get_action('group_list')({}, {'all_fields': True, 'sort': 'packages'})
    return groups[:num]


def showcases(num=24):
    """Return a list of showcases"""
    sorted_showcases = []
    try:
        showcases = toolkit.get_action('ckanext_showcase_list')({},{})
        sorted_showcases = sorted(showcases, key=lambda k: k.get('metadata_modified'), reverse=True)
    except:
        print "[guilfordnc_theme] Error in retrieving list of showcases"
    return sorted_showcases[:num]


def get_package_metadata(package):
    """Return the metadata of a dataset"""
    result = toolkit.get_action('package_show')(None, {'id': package.get('name'), 'include_tracking': True})
    return result


class Guilfordnc_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'guilfordnc_theme')

    # ITemplateHelpers

    def get_helpers(self):
        """Register guilfordnc_theme_* helper functions"""
        
        return {'guilfordnc_theme_recent_datasets': recent_datasets,
                'guilfordnc_theme_popular_datasets': popular_datasets,
                'guilfordnc_theme_dataset_count': dataset_count,
                'guilfordnc_theme_get_groups': groups,
                'guilfordnc_theme_get_showcases': showcases,
                'guilfordnc_theme_get_package_metadata': get_package_metadata}