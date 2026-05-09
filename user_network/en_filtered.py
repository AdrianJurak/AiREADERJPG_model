import torch.nn as nn
from modules.transformation import TPS_SpatialTransformerNetwork
from modules.feature_extraction import VGG_FeatureExtractor, RCNN_FeatureExtractor, ResNet_FeatureExtractor
from modules.sequence_modeling import BidirectionalLSTM
from modules.prediction import Attention
import torch.nn.functional as F

class Model(nn.Module):

    def __init__(self, input_channel, num_class, **kwargs):
        super(Model, self).__init__()

        # Pancerne ustawienia - takie same na jakich trenowałeś
        class AttrDict(dict):
            def __getattr__(self, name):
                return self.get(name, None)

            def __setattr__(self, name, value):
                self[name] = value

        # Łączymy to co przysłał EasyOCR z domyślnymi wartościami
        opt = AttrDict()
        opt.Transformation = kwargs.get('Transformation', 'None')
        opt.FeatureExtraction = kwargs.get('FeatureExtraction', 'VGG')
        opt.SequenceModeling = kwargs.get('SequenceModeling', 'BiLSTM')
        opt.Prediction = kwargs.get('Prediction', 'CTC')
        opt.num_fiducial = kwargs.get('num_fiducial', 20)
        opt.imgH = kwargs.get('imgH', 64)
        opt.imgW = kwargs.get('imgW', 600)
        opt.input_channel = kwargs.get('input_channel', 1)
        opt.output_channel = kwargs.get('output_channel', 256)
        opt.hidden_size = kwargs.get('hidden_size', 256)
        opt.batch_max_length = kwargs.get('batch_max_length', 100)

        self.opt = opt
        self.stages = {'Trans': opt.Transformation, 'Feat': opt.FeatureExtraction,
                       'Seq': opt.SequenceModeling, 'Pred': opt.Prediction}

        """ Transformation """
        if opt.Transformation == 'TPS':
            self.Transformation = TPS_SpatialTransformerNetwork(
                F=20, I_size=(100, 1000), I_r_size=(100, 1000), I_channel_num=input_channel)
        else:
            pass

        """ FeatureExtraction """
        if opt.FeatureExtraction == 'VGG':
            self.FeatureExtraction = VGG_FeatureExtractor(opt.input_channel, opt.output_channel)
        elif opt.FeatureExtraction == 'RCNN':
            self.FeatureExtraction = RCNN_FeatureExtractor(opt.input_channel, opt.output_channel)
        elif opt.FeatureExtraction == 'ResNet':
            self.FeatureExtraction = ResNet_FeatureExtractor(opt.input_channel, opt.output_channel)

        self.FeatureExtraction_output = opt.output_channel
        self.AdaptiveAvgPool = nn.AdaptiveAvgPool2d((None, 1))

        """ Sequence modeling"""
        if opt.SequenceModeling == 'BiLSTM':
            self.SequenceModeling = nn.Sequential(
                BidirectionalLSTM(self.FeatureExtraction_output, opt.hidden_size, opt.hidden_size),
                BidirectionalLSTM(opt.hidden_size, opt.hidden_size, opt.hidden_size))
            self.SequenceModeling_output = opt.hidden_size
        else:
            self.SequenceModeling_output = self.FeatureExtraction_output

        """ Prediction """
        if opt.Prediction == 'CTC':
            self.Prediction = nn.Linear(self.SequenceModeling_output, num_class)
        elif opt.Prediction == 'Attn':
            self.Prediction = Attention(self.SequenceModeling_output, opt.hidden_size, num_class)

    def forward(self, input, text, is_train=True):
        """ Transformation stage """
        # --- MAGICZNY FIX PADDINGU (Sztuczne poszerzanie dla modelu) ---
        b, c, h, w = input.size()
        if w != 1000:
            pad_right = 1000 - w
            if pad_right > 0:
                # Jeśli obraz jest węższy niż 1000px, dorabiamy puste tło z prawej strony
                input = F.pad(input, (0, pad_right, 0, 0), "constant", 0)
            else:
                # Jeśli jest jakimś cudem szerszy, zwężamy go
                input = F.interpolate(input, size=(100, 1000), mode='bicubic', align_corners=True)
        # ---------------------------------------------------------------

        """ Feature extraction stage """
        visual_feature = self.FeatureExtraction(input)
        visual_feature = self.AdaptiveAvgPool(visual_feature.permute(0, 3, 1, 2))
        visual_feature = visual_feature.squeeze(3)

        """ Sequence modeling stage """
        if self.stages['Seq'] == 'BiLSTM':
            contextual_feature = self.SequenceModeling(visual_feature)
        else:
            contextual_feature = visual_feature

        """ Prediction stage """
        if self.stages['Pred'] == 'CTC':
            prediction = self.Prediction(contextual_feature.contiguous())
        else:
            prediction = self.Prediction(contextual_feature.contiguous(), text, is_train, batch_max_length=self.opt.batch_max_length)

        return prediction