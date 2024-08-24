import pytest

from photo_agent.environment import PhotoEnvironment


def test_init_from_config():
    config = {
        "camera": {
            "position": {"x": 10, "y": 5, "z": 15},
            "iso": 800,
            "shutter_speed": 1 / 200,
            "aperture": 8,
        },
        "subject": {"position": {"x": 5, "y": 5, "z": 5}},
        "lights": [
            {
                "variant": "STROBE",
                "position": {"x": 15, "y": 10, "z": 5},
                "angle": 45,
                "config": {"power": 1200, "intensity": 1, "speed": 1 / 800},
                "modifier": {
                    "variant": "SOFTBOX",
                    "config": {"height": 50, "width": 50},
                },
                "filters": [{"variant": "GEL", "config": {"color": "blue"}}],
            }
        ],
    }
    environment = PhotoEnvironment.from_config(config)

    # Assert camera properties


def test_get_english_description():
    config = {
        "camera": {
            "position": {"x": 10, "y": 5, "z": 15},
            "iso": 800,
            "shutter_speed": 1 / 200,
            "aperture": 8,
        },
        "subject": {"position": {"x": 5, "y": 5, "z": 5}},
        "lights": [
            {
                "variant": "STROBE",
                "position": {"x": 15, "y": 10, "z": 5},
                "angle": 45,
                "config": {"power": 1200, "intensity": 1, "speed": 1 / 800},
                "modifier": {
                    "variant": "SOFTBOX",
                    "config": {"height": 50, "width": 50},
                },
                "filters": [{"variant": "GEL", "config": {"color": "blue"}}],
            }
        ],
    }

    # Create a PhotoEnvironment instance from the config
    env = PhotoEnvironment.from_config(config)

    # Get the English description
    description = env.get_english_description()

    # Expected description
    expected_description = (
        "The camera is at position (10, 5, 15) with ISO 800, aperture 8 and shutter speed 0.005. "
        "The subject is at position (5, 5, 5). "
        "There is 1 light in the environment. "
        "Light 1 is a Strobe light at position (15, 10, 5) with angle 45 degrees. "
        "The light has power 1200, intensity 1, and speed 0.00125. "
        "It has a Softbox modifier with height 50 and width 50. "
        "It has the following filters: Gel filter of color blue. "
    )

    # Assert that the generated description matches the expected description
    assert description == expected_description

    # Test with no lights
    config_no_lights = config.copy()
    config_no_lights["lights"] = []
    env_no_lights = PhotoEnvironment.from_config(config_no_lights)
    no_lights_description = env_no_lights.get_english_description()
    expected_no_lights_description = (
        "The camera is at position (10, 5, 15) with ISO 800, aperture 8 and shutter speed 0.005. "
        "The subject is at position (5, 5, 5). "
        "There are no lights in the environment."
    )
    assert no_lights_description == expected_no_lights_description

    # Test with multiple lights
    config_multi_lights = config.copy()
    config_multi_lights["lights"].append(
        {
            "variant": "STROBE",
            "position": {"x": 20, "y": 20, "z": 10},
            "angle": 30,
            "config": {"power": 1000, "intensity": 0.5, "speed": 1 / 1000},
        }
    )
    env_multi_lights = PhotoEnvironment.from_config(config_multi_lights)
    multi_lights_description = env_multi_lights.get_english_description()
    assert "There are 2 lights in the environment." in multi_lights_description
    assert "Light 1 is a Strobe light" in multi_lights_description
    assert "Light 2 is a Strobe light" in multi_lights_description
