from .amqp_pipeline import AMQPPipeline
from .mongo_pipeline import MongoPipeline
from .preprocess_pipeline import PreprocessPipeline
from .flow_pipeline import FlowPipeline


PREPROCESS_PIPELINE = 'scrapy_nc.pipelines.PreprocessPipeline'
AMQP_PIPELINE = 'scrapy_nc.pipelines.AMQPPipeline'
MONGO_PIPELINE = 'scrapy_nc.pipelines.MongoPipeline'
FLOW_PIPELINE = 'scrapy_nc.pipelines.FlowPipeline'

DEFAULT_PIPELINES = {
    PREPROCESS_PIPELINE: 500,
    MONGO_PIPELINE: 700,
    FLOW_PIPELINE: 760,
}
