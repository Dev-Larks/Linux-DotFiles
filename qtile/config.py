# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
#from libqtile.utils import guess_terminal

mod = "mod4"
mod1 = "alt"
#terminal = guess_terminal()
myTerminal = "alacritty"


def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)
    
def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


keys = [

    # Launch terminal, kill window, restart and exit Qtile

    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),


    # Rofi
    Key([mod, "mod1"], "space", lazy.spawn("rofi -modi run -show run -show-icons")),
    
    
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    #Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    #Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    #Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    #Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    #Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
        

    # Keybindings for applications
    Key([mod], "b", lazy.spawn("brave-browser"), desc="Launch Brave Browser"),
    Key([mod], "x", lazy.spawn("keepassxc"), desc="Launch Keepass"),

]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Columns(border_focus_stack='#d75f5f'),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

   # Bar colours

def init_colors():
    return [["#2E3440", "#2E3440"], # color 0
            ["#2E3440", "#2E3440"], # color 1
            ["#c0c5ce", "#c0c5ce"], # color 2
            ["#fba922", "#fba922"], # color 3
            ["#3384d0", "#3384d0"], # color 4
            ["#f3f4f5", "#f3f4f5"], # color 5
            ["#cd1f3f", "#cd1f3f"], # color 6
            ["#62FF00", "#62FF00"], # color 7
            ["#6790eb", "#6790eb"], # color 8
            ["#a9a9a9", "#a9a9a9"]] # color 9


colors = init_colors()


   # Widgets

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(
                	font = "UbuntuMono Nerd Font",
			fontsize = 14,
                        foreground = colors[5],
                        background = colors[1]                
                ),
                widget.GroupBox(
                        fontsize = 14,
                        margin_y = 3,
                        margin_x = 0,
                        padding_y = 6,
                        padding_x = 5,
                        borderwidth = 0,
                        disable_drag = True,
                        active = colors[9],
                        inactive = colors[5],
                        rounded = False,
                        highlight_method = "text",
                        this_current_screen_border = colors[8],
                        foreground = colors[2],
                        background = colors[1]
                ),
                widget.Prompt(),
                widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
                widget.WindowName(
                	font = "UbuntuMono Nerd Font",
			fontsize = 14,
                        foreground = colors[2],
                        background = colors[1]                
                ),
                #widget.Chord(
                #    chords_colors={
                #        'launch': ("#ff0000", "#ffffff"),
                #    },
                #    name_transform=lambda name: name.upper(),
                #),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                #widget.Systray(),
                widget.Sep(
                        linewidth = 1,
                        padding = 20,
                        foreground = colors[2],
                        background = colors[1]
                        ),
                widget.TextBox(
                        text = "NET:",
                        padding = 2,
                        foreground = colors[5],
                        background = colors[1],
                        fontsize = 14
                        ),
                widget.Net(
                        foreground = colors[2],
                        background = colors[1],
                        fontsize = 14
                	),
                widget.Sep(
                        linewidth = 1,
                        padding = 20,
                        foreground = colors[2],
                        background = colors[1]
                        ),
                widget.TextBox(
                        text = "UPDATES:",
                        padding = 2,
                        foreground = colors[5],
                        background = colors[1],
                        fontsize = 14
                        ),
                widget.CheckUpdates(
                        foreground = colors[2],
                        background = colors[1],
                        no_update_string = '0',
                        #distro = 'Pop!_OS',
                        fontsize = 14
                	),
                widget.Sep(
                        linewidth = 1,
                        padding = 20,
                        foreground = colors[2],
                        background = colors[1]
                        ),
                widget.TextBox(
                        text = "MEM:",
                        padding = 2,
                        foreground = colors[5],
                        background = colors[1],
                        fontsize = 14
                        ),
                widget.Memory(
                        #font="UbuntuMono Nerd Font",
                        format = '{MemUsed}M / {MemTotal}M ',
                        update_interval = 1.0,
                        fontsize = 14,
                        foreground = colors[2],
                        background = colors[1]
                        ),
                widget.Sep(
                        linewidth = 1,
                        padding = 20,
                        foreground = colors[2],
                        background = colors[1]
                        ),
                widget.TextBox(
                        text = "CPU:",
                        padding = 2,
                        foreground = colors[5],
                        background = colors[1],
                        fontsize = 14
                        ),
                widget.CPU(
			format = '{load_percent}% ',
			font = "UbuntuMono Nerd Font",
			fontsize = 14,
			foreground = colors[2],
                        background = colors[1],
                        update_interval = 3
			),
                widget.ThermalSensor(
                	font = "UbuntuMono Nerd Font",
                	fontsize = 14,
                	foreground = colors[2],
                	background = colors[1],
                	tag_sensor = "Core 1",
                	threshold = 90,
                	padding = 5
                ),
                widget.Sep(
                        linewidth = 1,
                        padding = 20,
                        foreground = colors[2],
                        background = colors[1]
                        ),
                widget.Clock(
                	font = "UbuntuMono Nerd Font",
                	fontsize = 14,
                	foreground = colors[5],
                	background = colors[1],
                	format='%Y-%m-%d  %a  %I:%M %p'
                        ),
                widget.Sep(
                        linewidth = 1,
                        padding = 20,
                        foreground = colors[2],
                        background = colors[1]
                        ),

                widget.QuickExit(
                	foreground = colors[2],
                        background = colors[1]
                	),
            ],
            24,
        ),
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    Match(wm_type='utility'),
    Match(wm_type='notification'),
    Match(wm_type='toolbar'),
    Match(wm_type='splash'),
    Match(wm_type='dialog'),
    Match(wm_class='file_progress'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
