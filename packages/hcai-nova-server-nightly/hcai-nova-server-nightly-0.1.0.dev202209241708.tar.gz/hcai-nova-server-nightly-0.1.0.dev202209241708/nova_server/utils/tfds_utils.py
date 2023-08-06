import sys
sys.path.append('/Users/Marco/Documents/Uni/Masterarbeit/hcai_datasets')

from hcai_datasets.hcai_nova_dynamic.hcai_nova_dynamic_iterable import HcaiNovaDynamicIterable


def dataset_from_request_form(request_form):
    """
    Creates a tensorflow dataset from nova dynamically
    :param request_form: the requestform that specifices the parameters of the dataset
    """
    db_config_dict = {
        'ip': request_form.get("server").split(':')[0],
        'port': int(request_form.get("server").split(':')[1]),
        'user': request_form.get("username"),
        'password': request_form.get("password")
    }

    ds_iter = HcaiNovaDynamicIterable(
        # Database Config
        db_config_path=None,  # os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.cfg'),
        db_config_dict=db_config_dict,

        # Dataset Config
        dataset=request_form.get("database"),
        nova_data_dir=request_form.get("dataPath"),
        sessions=request_form.get("sessions").split(';'),
        roles=request_form.get("roles").split(';'),
        schemes=request_form.get("scheme").split(';'),
        annotator=request_form.get("annotator"),
        data_streams=request_form.get("stream").split(' '),

        # TODO MARCO: Werte von unten dürfen nicht hard codiert sein requeste_form muss in nova erweitert werden, damit diese werte auch übergeben werden
        # Sample Config
        frame_size=0.04,
        left_context=request_form.get("leftContext"),
        right_context=request_form.get("rightContext"),
        start=0,
        end=request_form.get("cmlbegintime"),
        flatten_samples=True,
        supervised_keys=[request_form.get("stream").split(' ')[0],
                         request_form.get("scheme").split(';')[0]],

        # Additional Config
        clear_cache=True,
    )

    return ds_iter
