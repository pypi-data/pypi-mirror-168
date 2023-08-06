# -*- coding: utf-8 -*-
# @Filename : exception
# @Date : 2022-07-27-11-17
# @Project: content-script-slack-block-builder


class BlockBuilerException(Exception):
    pass


# Slack Block Builder Relevant Exception
class SlackBlocksBuilderException(BlockBuilerException):
    pass


class SlackBodyTypeError(SlackBlocksBuilderException):
    pass


class BlockSurfaceNotSupportError(SlackBlocksBuilderException):
    pass


class BlockElementOutOfRangeError(SlackBlocksBuilderException):
    pass


class BlockTypeError(SlackBlocksBuilderException):
    pass


class BlockMinimumOneElementError(SlackBlocksBuilderException):
    pass


class BlockValueError(SlackBlocksBuilderException):
    pass
