def get_optimizer_params(model, encoder_lr, decoder_lr, weight_decay=0.0):
    param_optimizer = list(model.named_parameters())
    no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
    optimizer_parameters = [
        {'params': [p for n, p in model.model.named_parameters() if not any(nd in n for nd in no_decay)],
         'lr': encoder_lr, 'weight_decay': weight_decay},
        {'params': [p for n, p in model.model.named_parameters() if any(nd in n for nd in no_decay)],
         'lr': encoder_lr, 'weight_decay': 0.0},
        {'params': [p for n, p in model.named_parameters() if "model" not in n],
         'lr': decoder_lr, 'weight_decay': 0.0}
    ]
    return optimizer_parameters


def get_optimizer_params_with_llrd(model, encoder_lr, decoder_lr, learning_rate_llrd_mult, weight_decay=0.0):
    named_parameters = list(model.named_parameters())
    no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
    optimizer_parameters = []

    init_lr = encoder_lr
    head_lr = decoder_lr
    lr = init_lr
    print(f'Learning Rates: \n\tHead LR: {init_lr}')

    # === Pooler and regressor ======================================================
    params_0 = [p for n, p in named_parameters if ("pooler" in n or "regressor" in n)
                and any(nd in n for nd in no_decay)]
    params_1 = [p for n, p in named_parameters if ("pooler" in n or "regressor" in n)
                and not any(nd in n for nd in no_decay)]

    head_params = {"params": params_0, "lr": head_lr, "weight_decay": 0.0}
    optimizer_parameters.append(head_params)

    head_params = {"params": params_1, "lr": head_lr, "weight_decay": weight_decay}
    optimizer_parameters.append(head_params)

    # === Hidden layers ==========================================================
    for layer in range(model.model_config.num_hidden_layers, -1, -1):
        params_0 = [p for n, p in named_parameters if f"encoder.layer.{layer}." in n
                    and any(nd in n for nd in no_decay)]
        params_1 = [p for n, p in named_parameters if f"encoder.layer.{layer}." in n
                    and not any(nd in n for nd in no_decay)]

        layer_params = {"params": params_0, "lr": lr, "weight_decay": 0.0}
        optimizer_parameters.append(layer_params)

        layer_params = {"params": params_1, "lr": lr, "weight_decay": weight_decay}
        optimizer_parameters.append(layer_params)
        print(f'\tLayer {layer} LR: {lr}')
        lr *= learning_rate_llrd_mult

    # === Embeddings layer ==========================================================
    print(f'\tEmbeddings LR: {lr}')
    params_0 = [p for n, p in named_parameters if "embeddings" in n
                and any(nd in n for nd in no_decay)]
    params_1 = [p for n, p in named_parameters if "embeddings" in n
                and not any(nd in n for nd in no_decay)]

    embed_params = {"params": params_0, "lr": lr, "weight_decay": 0.0}
    optimizer_parameters.append(embed_params)

    embed_params = {"params": params_1, "lr": lr, "weight_decay": weight_decay}
    optimizer_parameters.append(embed_params)

    return optimizer_parameters

