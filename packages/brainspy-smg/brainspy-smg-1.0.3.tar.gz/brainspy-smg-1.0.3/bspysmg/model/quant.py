import os
import torch
from brainspy.processors.simulation.model import NeuralNetworkModel
from bspysmg.model.training import postprocess
from brainspy.utils.io import create_directory_timestamp
from bspysmg.data.dataset import get_dataloaders

from brainspy.utils.pytorch import TorchUtils
from pytorch_memlab import MemReporter


class QuantModel(torch.nn.Module):
    def __init__(self, model):
        super(QuantModel, self).__init__()
        self.model = model
        self.quant = torch.quantization.QuantStub()
        self.dquant = torch.quantization.DeQuantStub()

    def forward(self, x):
        x = self.quant(x)
        x = self.model(x)
        x = self.dquant(x)
        return x


def quantize_model(configs, model_dir, model_name, quantize=True):

    results_dir = create_directory_timestamp(model_dir, 'quant')

    model_data = torch.load(os.path.join(model_dir, model_name),
                            map_location=torch.device('cpu'))
    model = TorchUtils.format(
        NeuralNetworkModel(model_data['info']['model_structure']))

    model.load_state_dict(model_data['model_state_dict'])

    #model = TorchUtils.format(model, device=torch.device('cpu'))
    #model = model.to(torch.device('cpu'))
    report_memory(model)
    dataloaders, amplification, _ = get_dataloaders(configs)
    # model_loss = postprocess(
    #     dataloaders[2],
    #     model,
    #     torch.nn.MSELoss(),
    #     amplification,
    #     results_dir,
    #     label='TEST',
    # )
    quant_model = QuantModel(model)
    quant_model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
    model.raw_model.qconfig = torch.quantization.get_default_qconfig(
        'fbgemm'
    )  #torch.quantization.default_qconfig  # get_default_qconfig('qnnpack')
    model.qconfig = torch.quantization.get_default_qconfig(
        'fbgemm'
    )  #torch.quantization.default_qconfig  # get_default_qconfig('qnnpack')
    torch.quantization.fuse_modules(
        quant_model.model.raw_model,
        [['0', '1'], ['2', '3'], ['4', '5'], ['6', '7'], ['8', '9']],
        inplace=True)
    torch.quantization.prepare(quant_model, inplace=True)
    torch.quantization.prepare(quant_model.model, inplace=True)
    torch.quantization.prepare(quant_model.model.raw_model, inplace=True)
    var = TorchUtils.format(torch.rand(4, 7))
    quant_model(var)
    #model.eval()
    # with torch.no_grad():
    #     for data, _ in dataloaders[2]:
    #         #data = TorchUtils.format(data)
    #         prepared_model(data.cpu())
    #prepared_model.eval()
    torch.quantization.convert(quant_model.model.raw_model, inplace=True)
    torch.quantization.convert(quant_model.model, inplace=True)
    torch.quantization.convert(quant_model, inplace=True)
    report_memory(quant_model)
    #report_memory(m2)
    qmodel_loss = postprocess(
        dataloaders[2],
        quant_model,
        torch.nn.MSELoss(),
        amplification,
        results_dir,
        label='TEST',
    )

    print('model_loss RMSE')
    print(model_loss)
    print('qmodel_loss RMSE')
    print(qmodel_loss)
    report_memory(qmodel_loss)


def report_memory(model):
    inp = TorchUtils.format(torch.rand([8, 7]))
    res = model(inp).mean()
    res.backward()
    reporter = MemReporter(model)
    reporter.report(verbose=True)


if __name__ == "__main__":
    TorchUtils.force_cpu = True
    from brainspy.utils.io import load_configs
    configs = load_configs('configs/training/smg_configs_template.yaml')

    quantize_model(
        configs,
        #"/home/unai/Documents/3-Programming/bspy/smg/tmp/output/conv_model/training_data_2021_10_19_153129/prunning_ammount_0.5_2021_10_20_213521",
        "/home/unai/Documents/3-Programming/bspy/smg/tmp",
        'training_data.pt')
