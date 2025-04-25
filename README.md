# Fire_Detect
![fire_flame_burn_139420_1920x1080](https://github.com/user-attachments/assets/16f993fc-69a9-4c4a-bbc9-20fc86d232b1)

We are a team working on improving an existing fire detector.

## Problem & Goal
- We already have a ready-made fire detector, but as we know nothing is perfect, so this detector has some problems. The main problem is false alarms on various sources of lights, flashers, etc. Our goal is to create a classification model that will process the output from the main model and finally determine whether it is a fire or not.

- У нас уже есть готовый детектор огня, но, как известно, нет ничего идеального, поэтому у этого детектора есть некоторые проблемы. Основная проблема - ложные срабатывания на различные источники света, мигалки и т. д. Наша цель - создать классификационную модель, которая будет обрабатывать выходные данные основной модели и в итоге определять, огонь это или нет.


## Solution
- Assemble a dataset with only images of fire and other various lighting sources that look like fire.
Find a classification model and train this model on the collected dataset, upload the model inference to the server and combine the two models.

- Собрать датасет, в котором будут только изображения огня и другие различные источники освещения, похожие на огонь.
Найти модель классификации и обучить данную модель на собранном датасете, загрузить инференс модели на сервер и совместить эти две модели.

## Metrics on test dataset
- precision 0.96
- recall 0.97
- accuracy 0.97

## Team
- [Ivan Sichkar](https://github.com/SichkarIvan)
- [Pavel Krylov](https://github.com/Ar1stok)
- [Danila Nazarov](https://github.com/shaman1641)
