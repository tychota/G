from dlgo.data.parallel_processor import GoDataProcessor

processor = GoDataProcessor(encoder='oneplane')
generator = processor.load_go_data('train', 10000, use_generator=True)

print(generator.get_num_samples())
generator = generator.generate(batch_size=10)

X, y = next(generator)
