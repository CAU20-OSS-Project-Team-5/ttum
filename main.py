import usecase_model

# excerpted from software engineering Ch.6 Use case page 3
# need to take out actor, scenario, use case
paragraph = """A customer arrives at a checkout with items to purchase. The 
cashier uses the POS system to record each purchased item. The system 
presents a running total and line-item details. The customer enters payment 
information, which the system validates and records. The system updates 
inventory. The customer receives a receipt from the system and then leaves 
with the items."""

if __name__ == '__main__':
    try:
        model = usecase_model.Model()
        model.train(5)
        model.restore_checkpoint()
        model.translate(u'checkout .')
    except (AttributeError, TypeError) as e:
        pass
