from __future__ import annotations

import pathlib

import colour
import pytest

from pyflp.channel import Channel, ChannelRack, Layer, Sampler


def test_channels(rack: ChannelRack):
    assert len(rack) == 18
    assert rack.fit_to_steps is None
    assert rack.height == 636
    assert [group.name for group in rack.groups] == ["Audio", "Generators", "Unsorted"]
    assert not rack.swing


@pytest.fixture(scope="session")
def channels(rack: ChannelRack):
    return tuple(rack)


@pytest.fixture(scope="session")
def layer(rack: ChannelRack):
    return tuple(rack.layers)[0]


@pytest.fixture(scope="session")
def samplers(rack: ChannelRack):
    return [s for s in rack.samplers]


def test_channel_name(channels: tuple[Channel]):
    assert tuple(channel.name for channel in channels) == (
        "BooBass",
        "Instrument track",
        "Layer",
        "Sampler",
        "Colored",
        "Automation Clip",
        "VST2",
        "Audio Clip",
        "Iconified",
        "Fruit Kick",
        "Plucked!",
        "22in Kick",
        "Zero Volume",
        "Full Volume",
        "100% L",
        "100% R",
        "Disabled",
        "Locked",
    )


def test_channel_color(channels: tuple[Channel, ...]):
    for channel in channels:
        if channel.name == "Colored":
            assert channel.color == colour.Color("#1414FF")
        elif channel.name in ("Audio track", "Instrument track"):
            # Colors are synced with insert and track
            assert channel.color == colour.Color("#485156")
        else:
            assert channel.color == colour.Color("#5C656A")


# TODO: Test `Channel.content`


def test_channel_enabled(channels: tuple[Channel, ...]):
    for ch in channels:
        assert not ch.enabled if ch.name == "Disabled" else ch.enabled


def test_channel_icon(channels: tuple[Channel, ...]):
    for ch in channels:
        assert ch.icon == 116 if ch.name == "Iconified" else not ch.icon


def test_layer_crossfade(layer: Layer):
    assert layer.crossfade


def test_layer_random(layer: Layer):
    assert layer.random


def test_sampler_path(samplers: tuple[Sampler, ...]):
    for sampler in samplers:
        if sampler.name == "22in Kick":
            # fmt: off
            assert sampler.sample_path == pathlib.Path(r"%FLStudioFactoryData%\Data\Patches\Packs\Drums\Kicks\22in Kick.wav")
            # fmt: on
        else:
            assert not sampler.sample_path
