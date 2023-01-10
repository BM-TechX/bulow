import os
import numpy as np

from detectron2.utils.logger import setup_logger
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.engine import default_setup, launch, default_argument_parser
from detectron2.config import get_cfg
from detectron2.data.datasets import register_coco_instances

from vibration_vials.engine.mytrainer import MyTrainer

def setup(args):
    """ CONFIG FILE FOR THE MODEL """
    path2config = "./configs/base_vibrationvials_semantic_config.yaml"
    cfg = get_cfg()
    cfg.merge_from_file(path2config)
    cfg.merge_from_list(args.opts)
    if cfg.SOLVER.LR_SCHEDULER_NAME == "WarmupPolyLR":
        cfg.SOLVER.POLY_LR_POWER = 0.9
        cfg.SOLVER.POLY_LR_CONSTANT_ENDING = 0.0
    if cfg.SOLVER.LR_SCHEDULER_NAME == "WarmupMultiStepLR":
        cfg.SOLVER.STEPS = (500, 1000, 1500)
        # cfg.SOLVER.WEIGHT_DECAY = 0.0005
    cfg.freeze()
    default_setup(cfg, args)
    return cfg

def main(args):
    path2train = "./data/train"
    path2valid = "./data/valid"
    path2images = "./data/images"

    register_coco_instances("train_dataset", {}, os.path.join(path2train, "coco_train.json"), path2images)
    register_coco_instances("valid_dataset", {}, os.path.join(path2valid, "coco_valid.json"), path2images)

    cfg = setup(args)
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

    if args.eval_only:
        model = MyTrainer.build_model(cfg)
        DetectionCheckpointer(model, save_dir=cfg.OUTPUT_DIR).resume_or_load(
            cfg.MODEL_WEIGHTS, resume=False
        )
        res = MyTrainer.test(cfg, model)
        return res
    
    trainer = MyTrainer(cfg)
    trainer.resume_or_load(resume=False)
    return trainer.train()

if __name__ == "__main__":
    args = default_argument_parser().parse_args()
    launch(
        main,
        args.num_gpus,
        num_machines=args.num_machines,
        machine_rank=args.machine_rank,
        dist_url=args.dist_url,
        args = (args,)
    )