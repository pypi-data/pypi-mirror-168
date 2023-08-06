import os
import torch
from brainspy.processors.simulation.model import NeuralNetworkModel
from torch.nn.utils import prune

# for i, module in model.raw_model.named_modules():
#     if i != '' and int(i) % 2 == 0:
#         prune.remove(model.raw_model[int(i)], 'weight')

# print(a)
from torch.optim import Adam
from torch.nn import MSELoss

from brainspy.utils.pytorch import TorchUtils
from brainspy.utils.io import create_directory_timestamp

from bspysmg.model.training import init_seed, train_loop
from bspysmg.data.dataset import get_dataloaders
from bspysmg.model.training import postprocess
import matplotlib.pyplot as plt

def prune_and_retrain(
    configs,
    model_folder='tmp/output/conv_model/training_data_2021_10_19_153129/prunning_ammount_0.5_2021_10_20_213521',
    pruning_ammount=[0.5],
    # custom_model=NeuralNetworkModel,
    criterion=MSELoss(),
    custom_optimizer=Adam,
    # main_folder="training_data",
):
    # Initialise seed and create data directories
    # init_seed(configs)
    results_dir = create_directory_timestamp(model_folder,
                                             'prunning_ammount_' + str(0.5))
    # Get training, validation and test data
    # Get amplification of the device and the info

    # Initilialise model

    training_data = torch.load(
        os.path.join(model_folder, "pruned_training_data.pt"))

    model = NeuralNetworkModel(training_data['info']['model_structure'])
    model.load_state_dict(training_data['model_state_dict'])

    for i in range(len(pruning_ammount)):
        parameters_to_prune = (
            (model.raw_model[0], 'weight'),
            (model.raw_model[2], 'weight'),
            (model.raw_model[4], 'weight'),
            (model.raw_model[6], 'weight'),
            (model.raw_model[8], 'weight'),
            (model.raw_model[10], 'weight'),
        )

        #prune.random_unstructured(model.raw_model[0], 'weight', 0.3)
        prune.global_unstructured(
            parameters_to_prune,
            pruning_method=prune.L1Unstructured,
            amount=pruning_ammount,
        )

        for i, module in model.raw_model.named_modules():
            if i != '' and int(i) % 2 == 0:
                print("Sparsity in module: {:.2f}%".format(
                    100. * float(torch.sum(module.weight == 0)) /
                    float(module.weight.nelement())))

        dataloaders, amplification, info_dict = get_dataloaders(configs)
        # model.set_info_dict(info_dict)
        model = TorchUtils.format(model)

        # Initialise optimiser
        optimizer = custom_optimizer(
            filter(lambda p: p.requires_grad, model.parameters()),
            lr=configs["hyperparameters"]["learning_rate"],
            betas=(0.9, 0.75),
        )

        # Whole training loop
        model, performances = train_loop(
            model,
            info_dict,
            (dataloaders[0], dataloaders[1]),
            criterion,
            optimizer,
            configs["hyperparameters"]["epochs"],
            amplification,
            save_dir=results_dir,
        )

        # Plot results
        labels = ["TRAINING", "VALIDATION", "TEST"]
        for i in range(len(dataloaders)):
            if dataloaders[i] is not None:
                loss = postprocess(
                    dataloaders[i],
                    model,
                    criterion,
                    amplification,
                    results_dir,
                    label=labels[i],
                )

        plt.figure()
        plt.plot(TorchUtils.to_numpy(performances[0]))
        if len(performances) > 1 and not len(performances[1]) == 0:
            plt.plot(TorchUtils.to_numpy(performances[1]))
        if dataloaders[-1].dataset.tag == 'test':
            plt.plot(np.ones(len(performances[-1])) * TorchUtils.to_numpy(loss))
            plt.title("Training profile /n Test loss : %.6f (nA)" % loss)
        else:
            plt.title("Training profile")
        if not len(performances[1]) == 0:
            plt.legend(["training", "validation"])
        plt.xlabel("Epoch no.")
        plt.ylabel("RMSE (nA)")
        plt.savefig(os.path.join(results_dir, "training_profile_"+str(i)))
        save_model(results_dir)
        


def save_model(results_dir):
    training_data = torch.load(
                os.path.join(results_dir, "training_data.pt"))
    training_data['masked_model_state_dict'] = model.state_dict()
    for i, module in model.raw_model.named_modules():
        if i != '' and int(i) % 2 == 0:
            prune.remove(model.raw_model[int(i)], 'weight')
    training_data['pruned_model_state_dict'] = model.state_dict()
    torch.save(training_data, os.path.join(model_folder,
                                        'pruned_training_data.pt'))
    print("Model saved in :" + results_dir)

def apply_prunning(model_dir: str):
    training_data = torch.load(os.path.join(model_dir, "training_data.pt"))
    model = NeuralNetworkModel(training_data['info']['model_structure'])

    parameters_to_prune = (
        (model.raw_model[0], 'weight'),
        (model.raw_model[2], 'weight'),
        (model.raw_model[4], 'weight'),
        (model.raw_model[6], 'weight'),
        (model.raw_model[8], 'weight'),
        (model.raw_model[10], 'weight'),
    )

    #prune.random_unstructured(model.raw_model[0], 'weight', 0.3)
    prune.global_unstructured(
        parameters_to_prune,
        pruning_method=prune.L1Unstructured,
        amount=0.5,
    )
    model.load_state_dict(training_data['model_state_dict'])
    for i, module in model.raw_model.named_modules():
        if i != '' and int(i) % 2 == 0:
            prune.remove(model.raw_model[int(i)], 'weight')

    training_data['model_state_dict'] = model.state_dict()
    torch.save(training_data, os.path.join(model_dir,
                                           'pruned_training_data.pt'))


if __name__ == "__main__":
    # from brainspy.utils.io import load_configs

    # configs = load_configs("configs/training/smg_configs_template.yaml")
    # prune_and_retrain(configs)
    # apply_prunning(
    #     "/home/unai/Documents/3-Programming/bspy/smg/tmp/output/conv_model/training_data_2021_10_19_153129/prunning_ammount_0.5_2021_10_20_213521"
    # )
