import torch
from utils import save_checkpoint, load_checkpoint, save_some_examples
import torch.nn as nn
import torch.optim as optim
import config
from dataset import MapDataset
from generator_model import Generator
from discriminator_model import Discriminator
from torch.utils.data import DataLoader
from tqdm import tqdm
from torchvision.utils import save_image

torch.backends.cudnn.benchmark = True


def train_fn(
    disc, gen, loader, opt_disc, opt_gen, l1_loss, bce, g_scaler, d_scaler, epoch,
):
    loop = tqdm(loader, leave=True)

    for idx, (x, y) in enumerate(loop):
        x = x.to(config.DEVICE)
        y = y.to(config.DEVICE)

        # Train Discriminator
        with torch.cuda.amp.autocast():
            y_fake = gen(x)
            # D_real = what discriminator outputs on the real image
            D_real = disc(x, y)
            # bce = max log(D(real) + log(1 - D(G(z)))      # (or min of negative)
            D_real_loss = bce(D_real, torch.ones_like(D_real))
            # D_fake = what discriminator outputs on the fake image (detach to retain computational graph on the generator step a few lines below (notice how we dont have to do y_fake again))
            D_fake = disc(x, y_fake.detach())
            D_fake_loss = bce(D_fake, torch.zeros_like(D_fake))
            D_loss = (D_real_loss + D_fake_loss) / 2

        disc.zero_grad()
        d_scaler.scale(D_loss).backward()
        d_scaler.step(opt_disc)
        d_scaler.update()

        # Train generator
        with torch.cuda.amp.autocast():
            # use y_fake to get D_fake like above
            D_fake = disc(x, y_fake)
            # again with bce but this time ones_like with the fake image unlike above -> min(1  - D(G(z)))
            G_fake_loss = bce(D_fake, torch.ones_like(D_fake))
            # did L1 loss in paper too
            L1 = l1_loss(y_fake, y) * config.L1_LAMBDA
            G_loss = G_fake_loss + L1

        opt_gen.zero_grad()
        g_scaler.scale(G_loss).backward()
        g_scaler.step(opt_gen)
        g_scaler.update()

        if idx % 5 == 0:
            loop.set_postfix(
                Epoch_NUM=epoch,
                D_real=torch.sigmoid(D_real).mean().item(),
                D_fake=torch.sigmoid(D_fake).mean().item(),
                #D_real_loss=D_real_loss,
                #D_fake_loss=D_fake_loss,
                #D_loss=D_loss,
                G_fake_loss=G_fake_loss,
                L1 = L1,
                #G_loss = G_loss,
            )


def main():
    disc = Discriminator(in_channels=4).to(config.DEVICE)
    gen = Generator(in_channels=4, features=64).to(config.DEVICE)
    opt_disc = optim.Adam(disc.parameters(), lr=config.LEARNING_RATE_DISC, betas=(0.5, 0.999),)
    opt_gen = optim.Adam(gen.parameters(), lr=config.LEARNING_RATE, betas=(0.5, 0.999))
    BCE = nn.BCEWithLogitsLoss()
    L1_LOSS = nn.L1Loss()


    if config.LOAD_MODEL:
        load_checkpoint(
            config.CHECKPOINT_GEN, gen, opt_gen, config.LEARNING_RATE,
        )
        load_checkpoint(
            config.CHECKPOINT_DISC, disc, opt_disc, config.LEARNING_RATE,
        )

    train_dataset = MapDataset(root_dir=config.TRAIN_DIR)
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        num_workers=config.NUM_WORKERS,
    )
    g_scaler = torch.cuda.amp.GradScaler()
    d_scaler = torch.cuda.amp.GradScaler()
    val_dataset = MapDataset(root_dir=config.VAL_DIR)
    # batch of how many images should be evaluated
    val_loader = DataLoader(val_dataset, batch_size=1, shuffle=False)

    for epoch in range(config.NUM_EPOCHS):
        train_fn(
            disc, gen, train_loader, opt_disc, opt_gen, L1_LOSS, BCE, g_scaler, d_scaler, epoch,
        )

        if config.SAVE_MODEL and ((epoch == 1) or (epoch == 5) or (epoch == 10) or (epoch == 25) or (epoch == 50) or (epoch == 100) or (epoch == 150) or (epoch == 199)):
            save_checkpoint(gen, opt_gen, filename="epoch_" + str(epoch) + config.CHECKPOINT_GEN)
            save_checkpoint(disc, opt_disc, filename="epoch_" + str(epoch) + config.CHECKPOINT_DISC)

        save_some_examples(gen, val_loader, epoch, folder="evaluation")


if __name__ == "__main__":
    main()