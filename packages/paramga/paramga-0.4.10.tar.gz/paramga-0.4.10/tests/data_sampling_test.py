

from paramga.data_sampling import generate_bootstrap_samples


class TestGenerateBootstrapSamples:

    def test_works_without_errors(self):
        generate_bootstrap_samples(3, 8)

    def test_outputs_correct_shape(self):
        out = generate_bootstrap_samples(3, 8)
        assert out.shape == (8,3)
