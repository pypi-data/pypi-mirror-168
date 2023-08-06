from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList
from sphinx_design import icons

__version__ = "0.0.1"


class ComponentIntro(Directive):
    has_content = False

    def run(self):
        # Use the state machine to generate a block quote for us and parse our text :)
        return self.state.block_quote(StringList([
            ":octicon:`light-bulb;1em;sd-text-info` New to components? Write your first one with :doc:`our guide </guides/components>`"
        ]), self.content_offset)


def setup(app):
    app.add_directive("bsb_component_intro", ComponentIntro)

    return {
        'version': '0.0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
