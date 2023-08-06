
def validation(data: dict) -> tuple:
    err_msg = ''
    is_valid = True
    if not data.get('filename'):
        err_msg = 'The filename is not provided.'
        is_valid = False
    if not data.get('class'):
        err_msg = 'The class data is not provided.'
        is_valid = False
    else:
        class_data = data.get('class')
        if not class_data.get('name'):
            err_msg = 'The class name is not provided.'
            is_valid = False
        if class_data.get('base_classes') and \
                not isinstance(class_data.get('base_classes'), list):
            err_msg = 'The base_classes are not provided in a list.'
            is_valid = False
        if class_data.get('class_attributes') and \
                not isinstance(class_data.get('class_attributes'), list):
            err_msg = 'The class_attributes are not provided in a list.'
            is_valid = False
        if class_data.get('instance_attributes') and \
                not isinstance(class_data.get('instance_attributes'), list):
            err_msg = 'The instance_attributes are not provided in a list.'
            is_valid = False
        instance_methods = class_data.get('instance_methods')
        if instance_methods:
            if not isinstance(instance_methods, list):
                err_msg = 'The instance_methods is not provided in a list.'
                is_valid = False
            else:
                for method in instance_methods:
                    if method.get('decorators') and \
                            not isinstance(method.get('decorators'), list):
                        err_msg = 'The instance_method decorators are not provided in a list.'
                        is_valid = False
                    if method.get('statements') and \
                            not isinstance(method.get('statements'), list):
                        err_msg = 'The instance_method statements are not provided in a list.'
                        is_valid = False
                    if method.get('arguments') and \
                            not isinstance(method.get('arguments'), list):
                        err_msg = 'The instance_method arguments are not provided in a list.'
                        is_valid = False
                    if not method.get('name'):
                        err_msg = 'The class method name is not provided.'
                        is_valid = False
                    if not method.get('return_type'):
                        err_msg = 'The class method return_type is not provided.'
                        is_valid = False
    return is_valid, err_msg
