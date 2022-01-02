# Map Synthesis for Low-Poly 3D Scenes using Generative Adversarial Networks

#### Info:
Bachelor Thesis about creating Video Game Maps procedurally using Generative Adversarial Networks. 

Contact: tobias.christoph@student.uibk.ac.at

For the creation of data `https://github.com/pecarprimoz/procedural-gen-dipl` was used to create height maps with according biomes. These maps were then analysed for traversability (`code/dataset/sketchify.py`) - which are the labels for the GAN and resemble the sketch a user can draw as an input. As base of the GAN Aladdin Persson's implementation `https://github.com/aladdinpersson/Machine-Learning-Collection/tree/master/ML/Pytorch/GANs/Pix2Pix` was used.

Weights used on the generated maps can be downloaded [here](https://github.com/teletobbii/map-synth-ba/releases/tag/v0.1)

The code to the finished project can be found here: [map-synth-ba/code/](https://github.com/teletobbii/map-synth-ba/tree/main/code). The scripts for the creation of the dataset creation as well as the creation of a traversability-map are under [map-synth-ba/code/scripts/dataset_creation/](https://github.com/teletobbii/map-synth-ba/tree/main/code/scripts/dataset_creation). 
Scripts to post-process the generated output are found here: [map-synth-ba/code/scripts/post/](https://github.com/teletobbii/map-synth-ba/tree/main/code/scripts/post).

All files regarding the Pix2Pix GAN are under [map-synth-ba/code/gan/pix2pix](https://github.com/teletobbii/map-synth-ba/tree/main/code/gan/pix2pix). Training files must be placed in the [train](https://github.com/teletobbii/map-synth-ba/tree/main/code/gan/pix2pix/data/train) folder (a sample of 1000 training files can already be found there). Specific settings can be made in the [config.py](https://github.com/teletobbii/map-synth-ba/tree/main/code/gan/pix2pix/config.py) file. To start training, run the [train.py](https://github.com/teletobbii/map-synth-ba/tree/main/code/gan/pix2pix/train.py) file. 


Topic description:
### Topic 2 - Map (Room/Terrain) Synthesis for Low-Poly 3D Scenes
Maps in 3D scenes and video games play a crucial role to determine the setting and player experience. Forming terrain or designing the outlines of rooms and order of locations in a map is a resource consuming task [1]. Thus, procedural content generation aims to alleviate the time and memory burden by automatically synthesising maps and artefacts.

The main goal of this Bachelor thesis comprises of generating low-poly maps w.r.t. to a certain style. The style is defined by input conditions such as text or rough sketches that are translated to labeled height or heat maps via deep learning and then transformed into a 3D scene via a deterministic parsing and rendering algorithm [1]. The most common deep learning model used for map synthesis are Generative Adversarial Networks (GANs) [2].

Thereby the maps can consist of a single room, multiple rooms or dungeons chained together, terrain or a combination of.
Styles could comprise settings (like fantasy) or map stylisations. In order to inject styles to the maps aside from mere layout choices, an extension to this thesis entails colouring and texturing the resulting low-poly maps.

To implement the map generation via deep learning the Unity Engine [3] is used for rendering and interacting with the scene, and Python's machine learning libraries (e.g. TensorFlow [4]) will be deployed to synthesise the height/heat maps. Although this topic is framed as a Bachelor thesis project, it can be extended to a Master thesis topic as well.

Tasks:
- Familiarise yourself with PCG and map generation and GANs
- Learn the ropes of the selected machine learning method
- Implement conditional hight/heat map generation
- Deploy a (deterministic) rendering method to obtain a low-poly 3D scene from the height/heat maps
- Test and extend to different types of maps
- Optionally extend method to allow for colouring and texturing maps w.r.t. styles

References:
[1] Liapis A., Yannakakis G.N., Togelius J. (2013) Sentient World: Human-Based Procedural Cartography. In: Machado P., McDermott J., Carballal A. (eds) Evolutionary and Biologically Inspired Music, Sound, Art and Design. EvoMUSART 2013. Lecture Notes in Computer Science, vol 7834. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-36955-1_16
[2] Ping K., Dingli L. (2020) Conditional Convolutional Generative Adversarial Networks Based Interactive Procedural Game Map Generation. In: Arai K., Kapoor S., Bhatia R. (eds) Advances in Information and Communication. FICC 2020. Advances in Intelligent Systems and Computing, vol 1129. Springer, Cham. https://doi.org/10.1007/978-3-030-39445-5_30
[3] Unity Engine https://unity.com
[4] TensorFlow https://www.tensorflow.org

