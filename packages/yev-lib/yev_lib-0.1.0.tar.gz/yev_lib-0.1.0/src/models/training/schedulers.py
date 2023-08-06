from transformers import get_linear_schedule_with_warmup, \
    get_cosine_schedule_with_warmup, \
    get_polynomial_decay_schedule_with_warmup


def get_scheduler(scheduler_type, optimizer, num_train_steps,
                  num_warmup_steps=0, num_cycles=0.5, power=1.0, min_lr=1e-7):

    if scheduler_type == 'linear':
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=num_warmup_steps,
            num_training_steps=num_train_steps
        )
    elif scheduler_type == 'cosine':
        scheduler = get_cosine_schedule_with_warmup(
            optimizer,
            num_warmup_steps=num_warmup_steps,
            num_training_steps=num_train_steps,
            num_cycles=num_cycles
        )
    elif scheduler_type == 'polynomial':
        scheduler = get_polynomial_decay_schedule_with_warmup(
            optimizer,
            num_warmup_steps=num_warmup_steps,
            num_training_steps=num_train_steps,
            power=power,
            lr_end=min_lr
        )
    else:
        raise ValueError(f'Unknown scheduler: {scheduler_type}')

    return scheduler
