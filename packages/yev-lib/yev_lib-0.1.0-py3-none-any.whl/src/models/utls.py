
def freeze(module):
    for parameter in module.parameters():
        parameter.requires_grad = False
