from enum import Enum
from PyQt6.QtCore import *

class Stylesheet(Enum):
    LIGHT = 0
    DARK = 1

class Stylesheets():
    def styles(self, base_path:str) -> dict[str,str]:
        self._transparent = ["transparent", "transparent"]
        self._color = ["#000000", "#FFFFFF"]
        self._color_disabled = ["#B0B0B0", "#5F5F5F"]
        self._color_combobox_disabled = ["#808080", "#7F7F7F"]
        self._border_top = ["#ABABAB", "#181818"]
        self._border_left = ["#ABABAB", "#181818"]
        self._border_bottom = ["#E7E7E7", "#545454"]
        self._border_right = ["#E7E7E7", "#545454"]
        self._menu_border = ["#ABABAB", "#545454"]
        self._gradiant_1_0 = ["#C8C8C8", "#373737"]
        self._gradiant_1_1 = ["#C1C1C1", "#3E3E3E"]
        self._gradiant_1_2 = ["#BDBDBD", "#424242"]
        self._gradiant_1_3 = ["#B6B6B6", "#494949"]
        self._gradiant_1_0_disabled = ["#A8A8A8", "#575757"]
        self._gradiant_1_1_disabled = ["#A1A1A1", "#5E5E5E"]
        self._gradiant_1_2_disabled = ["#9D9D9D", "#626262"]
        self._gradiant_1_3_disabled = ["#969696", "#696969"]
        self._gradiant_border_1_1 = ["#D8D8D8", "#272727"]
        self._gradiant_border_1_2 = ["#C9C9C9", "#363636"]
        self._gradiant_border_1_3 = ["#BABABA", "#454545"]
        self._frame_color = ["#DCDCDC", "#232323"]
        self._frame_selected_color = ["#BABABA", "#454545"]
        self._button_color = ["#BFBFBF", "#404040"]
        self._button_disabled_color = ["#CFCFCF", "#303030"]
        self._button_color_clicked = ["#AFAFAF", "#505050"]
        self._button_color_hovered = ["#CFCFCF", "#303030"]
        self._button_switch = ["#11AAEE", "#EE4444"]
        self._button_switch_color_clicked = ["#0099DD", "#FF5555"]
        self._button_switch_color_hovered = ["#22BBFF", "#DD3333"]
        self._selection_background = ["#00AAFF", "#FF4444"]
        self._tab_color = ["#D3D3D3", "#2C2C2C"]
        self._tab_selected_color = ["#646464", "#9B9B9B"]
        self._pane_color = ["#D3D3D3", "#2C2C2C"]
        self._gradiant_tab_1_1 = ["#D8D8D8", "#272727"]
        self._gradiant_tab_1_2 = ["#E3E3E3", "#1C1C1C"]
        self._header_color = ["#CFCFCF", "#303030"]
        self._switch_off = ["#AAAAAA", "#555555"]
        self._switch_on = ["#00AAFF", "#FF4444"]
        self._switch_disabled = ["#CBCBCB", "#343434"]
        self._switch_handle = ["#FFFFFF", "#000000"]
        self._switch_handle_disabled = ["#BBBBBB", "#444444"]
        self._slider_handle_color = ["#DFDFDF", "#202020"]
        self._slider_handle_border = ["#9F9F9F", "#7C7C7C"]
        self._slider_handle_color_disabled = ["#BFBFBF", "#404040"]
        self._slider_handle_color_pressed = ["#FFFFFF", "#000000"]
        self._color_background = ["#C6C6C6", "#393939"]
        self._color_light = ["#D0D0D0", "#2f2f2f"]
        self._color_dark = ["#D6D6D6", "#292929"]
        self._node_brush_title = ["#FFCECECE", "#FF313131"]
        self._node_brush_background = ["#E3DEDEDE", "#E3212121"]
        self._node_pen_default = ["#E3DEDEDE", "#E3212121"]
        self._title_color = [Qt.GlobalColor.black, Qt.GlobalColor.white]
        self._socket_pen = ["#FFFFFFFF", "#FF000000"]
        self._socket_pen_disabled = ["#FFFFFFFF", "#FF000000"]
        self._edge_pen_default = ["#FF222222", "#FFDDDDDD"]
        self._branch_closed = ["light_branch_closed", "dark_branch_closed"]
        self._branch_open = ["light_branch_open", "dark_branch_open"]
        self._branch_more = ["light_branch_more", "dark_branch_more"]
        self._branch_end = ["light_branch_end", "dark_branch_end"]
        self._checkmark = ["light_checkbox.png", "dark_checkbox.png"]
        self._important = ["light_important.png", "dark_important.png"]
        self._settings = ["light_settings.png", "dark_settings.png"]
        self._light_mode = ["light_light_mode.png", "dark_light_mode.png"]
        self._dark_mode = ["light_dark_mode.png", "dark_dark_mode.png"]
        self._info = ["light_info.png", "dark_info.png"]

        base_path = "/".join(base_path.split("\\")) + "/resources"
        return { "LIGHT":self.create_style(base_path, 0), "DARK":self.create_style(base_path, 1)}

    def create_style(self, base_path:str, index:int) -> str:
        style = f"""#frame{{ 
                background : {self._frame_color[index]}; 
                color : {self._color[index]}; 
            }}
            SettingsMenu {{ 
                background : {self._frame_color[index]}; 
                color : {self._color[index]}; 
                border-top : 2px solid {self._border_top[index]}; 
                border-left : 2px solid {self._border_left[index]}; 
                border-bottom : 2px solid {self._border_bottom[index]}; 
                border-right : 2px solid {self._border_right[index]};
                border-radius : 3px;
            }}
            QScrollArea {{ 
                background : transparent;
                border-top : 1px solid {self._border_top[index]}; 
                border-left : 1px solid {self._border_left[index]}; 
                border-bottom : 1px solid {self._border_top[index]}; 
                border-right : 1px solid {self._border_left[index]};
                border-radius : 3px;
            }}
            #settings{{
                background : {self._frame_color[index]}; 
                color : {self._color[index]}; 
                border : none;
                border-radius : 5px;
            }}
            QListWidget::item:selected {{
                font : bold; 
            }}
            QListview::item:selected {{
                font : bold; 
            }}
            QGraphicsTextItem{{
                background : transparent;
                font-weight : bold;
                color : {self._color[index]};
            }}
            QDMGraphicsView {{
                border-top : 2px solid {self._border_top[index]}; 
                border-left : 2px solid {self._border_left[index]}; 
                border-bottom : 2px solid {self._border_bottom[index]}; 
                border-right : 2px solid {self._border_right[index]};

            }}
            QMenu {{
                background : {self._frame_color[index]};
                border : 1px solid {self._menu_border[index]};
                color : {self._color[index]};
                border-radius : 3px;
                padding : 10px;
                text-align : center;
            }}
            QMenu::item {{
                border-bottom : 1px solid {self._menu_border[index]}; 
                text-align : center;
                padding : 3px;
            }}
            QMenu::item:disabled {{
                border-bottom : 3px solid {self._menu_border[index]}; 
                text-align : center;
                padding : 3px;
                font-weight : bold;
            }}
            QMenu::item:selected:enabled {{
                background : {self._menu_border[index]};
                font-weight : bold;
                text-align : center;
            }}
            QLabel {{
                background : transparent;
                font-weight : bold;
                color : {self._color[index]};
            }}
            QComboBox {{
                border-top : 1px solid {self._border_top[index]}; 
                border-left : 1px solid {self._border_left[index]}; 
                border-bottom : 1px solid {self._border_bottom[index]}; 
                border-right : 1px solid {self._border_right[index]};
                color : {self._color[index]};
                padding-right : 20px;
                padding-left : 10px;
            }}
            QComboBox:!editable {{
                background : qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1,
                                            stop : 0 {self._gradiant_1_0[index]}, stop : 0.4 {self._gradiant_1_1[index]},
                                            stop : 0.5 {self._gradiant_1_2[index]}, stop : 1.0 {self._gradiant_1_3[index]});
            }}
            /* QComboBox gets the "on" state when the popup is open */
            QComboBox:!editable:on {{
                background : qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1,
                                            stop : 0 {self._gradiant_1_3[index]}, stop : 0.4 {self._gradiant_1_2[index]},
                                            stop : 0.5 {self._gradiant_1_1[index]}, stop : 1.0 {self._gradiant_1_0[index]});
            }}
            QComboBox:disabled {{
                border-top : 1px solid {self._border_top[index]}; 
                border-left : 1px solid {self._border_left[index]}; 
                border-bottom : 1px solid {self._border_bottom[index]}; 
                border-right : 1px solid {self._border_right[index]};
                color : {self._color_combobox_disabled[index]};
                padding-right : 20px;
                padding-left : 10px;
            }}
            QComboBox:!editable:disabled {{
                background : qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1,
                                            stop : 0 {self._gradiant_1_0_disabled[index]}, stop : 0.4 {self._gradiant_1_1_disabled[index]},
                                            stop : 0.5 {self._gradiant_1_2_disabled[index]}, stop : 1.0 {self._gradiant_1_3_disabled[index]});
            }}
            QComboBox::drop-down:button{{
                border : none;
                background : transparent;
            }}
            QComboBox:down-arrow {{
                image : url({base_path}/{self._branch_open[index]}.png);
                padding-right : 10px;
            }}
            QPushButton {{
                background : {self._button_color[index]};
                font-weight : bold;
                height : 30px;
                color : {self._color[index]};
                border-radius : 3px;
                padding-right : 5px;
                padding-left : 5px;
                border-top : 1px solid {self._border_bottom[index]}; 
                border-left : 1px solid {self._border_right[index]}; 
                border-bottom : 1px solid {self._border_top[index]}; 
                border-right : 1px solid {self._border_left[index]};
            }}
            QPushButton:pressed {{
                background : {self._button_color_clicked[index]};
                border-top : 1px solid {self._border_top[index]}; 
                border-left : 1px solid {self._border_left[index]}; 
                border-bottom : 1px solid {self._border_bottom[index]}; 
                border-right : 1px solid {self._border_right[index]};
            }}
            QPushButton:hover:!pressed {{
                background : {self._button_color_hovered[index]};
                border-top : 1px solid {self._border_bottom[index]}; 
                border-left : 1px solid {self._border_right[index]}; 
                border-bottom : 1px solid {self._border_top[index]}; 
                border-right : 1px solid {self._border_left[index]};
            }}
            QPushButton:disabled, QPushButton:disabled[State] {{
                background : {self._button_disabled_color[index]};
                font-weight : bold;
                height : 30px;
                color : {self._color_disabled[index]};
                border-radius : 3px;
                padding-right : 5px;
                padding-left : 5px;
                border-top : 1px solid {self._border_bottom[index]}; 
                border-left : 1px solid {self._border_right[index]}; 
                border-bottom : 1px solid {self._border_top[index]}; 
                border-right : 1px solid {self._border_left[index]};
            }}
            QPushButton[State]{{
                background-color : {self._button_switch[index]};
            }}
            QPushButton[State]:pressed{{
                background-color : {self._button_switch_color_clicked[index]};
            }}
            QPushButton[State]:hover:!pressed{{
                background-color : {self._button_switch_color_hovered[index]};
            }}
            QCheckBox:disabled {{
                width : 14 px;
                height : 14 px;
            }}
            QCheckBox::indicator:disabled {{
                width : 14 px;
                height : 14 px;
            }}
            QCheckBox::indicator:disabled:unchecked {{
                border-radius : 3px;
                background-color : {self._button_color[index]};
                image : none;
            }}
            QCheckBox::indicator:disabled:checked {{
                border-radius : 3px;
                background-color : {self._switch_on[index]};
                image : url({base_path}/{self._checkmark[index]});
            }}
            QCheckBox::indicator[important="True"]:disabled {{
                border : none;
                background-color : transparent;
                image : url({base_path}/{self._important[index]});
            }}
            QCheckBox::indicator[important="False"]:disabled {{
                border : none;
                background-color : transparent;
                image : none;
            }}
            QTabBar::tab {{ 
                background-color : {self._tab_color[index]};
                color : {self._color[index]};
                border-top : 2px solid {self._border_top[index]};
                border-left : 2px solid {self._border_left[index]};
                border-right : 2px solid {self._border_right[index]}; 
                border-top-right-radius : 3px; 
                border-top-left-radius : 3px; 
                font-weight : bold;
                text-align : center;
                padding : 6px;
            }} 
            QTabWidget::pane {{ 
                background-color : {self._pane_color[index]}; 
                color : {self._color[index]};
                border-top : 2px solid {self._border_top[index]}; 
                border-left : 2px solid {self._border_left[index]}; 
                border-bottom : 2px solid {self._border_bottom[index]}; 
                border-right : 2px solid {self._border_right[index]}; 
                border-radius : 3px;
            }}
            QTabWidget::tab-bar {{
                alignment : center
            }}
            QHeaderView::section {{
                background-color : {self._header_color[index]};
                color : {self._color[index]};
                border : none;
                border-bottom : 1px solid qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0,
                stop : 0 {self._border_left[index]}, stop : 0.25 {self._gradiant_border_1_1[index]}, 
                stop : 0.5 {self._gradiant_border_1_2[index]}, stop : 0.75 {self._gradiant_border_1_3[index]}, 
                stop : 1.0 {self._border_right[index]});; 
                font-weight : bold;
                text-align : center;
            }}
            QTabBar::tab:selected, QTabBar::tab:hover {{
                background : qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1,
                stop : 0 {self._tab_color[index]}, stop : 0.4 {self._gradiant_tab_1_1[index]},
                stop : 0.5 {self._gradiant_tab_1_2[index]}, stop : 1.0 {self._tab_color[index]});
            }}
            QTabBar::tab:selected {{
                border-color : {self._tab_selected_color[index]};
                border-bottom-color : {self._pane_color[index]}; /* same as pane color */
            }}
            QTabBar::tab:!selected {{
                margin-top : 2px; /* make non-selected tabs look smaller */
            }}
            /* make use of negative margins for overlapping tabs */
            QTabBar::tab:selected {{
                /* expand/overlap to the left and right by 4px */
                margin-left : -4px;
                margin-right : -4px;
            }}
            QTabBar::tab:first:selected {{
                margin-left : 0; /* the first selected tab has nothing to overlap with on the left */
            }}
            QTabBar::tab:last:selected {{
                margin-right : 0; /* the last selected tab has nothing to overlap with on the right */
            }}
            QTabBar::tab:only-one {{
                margin : 0; /* if there is only one tab, we don't want overlapping margins */
            }}
            QTreeView, QListView, QTextEdit, QLineEdit {{
                background-color : {self._tab_color[index]}; 
                color : {self._color[index]};
                selection-background-color : {self._selection_background[index]};
                border-top : 2px solid {self._border_top[index]}; 
                border-left : 2px solid {self._border_left[index]};
                border-bottom : 2px solid {self._border_bottom[index]}; 
                border-right : 2px solid {self._border_right[index]}; 
                border-radius : 3px;
            }}
            QTreeView:disabled, QListView:disabled, QTextEdit:disabled, QLineEdit:disabled {{
                color : {self._color_disabled[index]};
            }}
            #info_text {{
                background-color : {self._tab_color[index]}; 
                color : {self._color[index]};
                selection-background-color : {self._selection_background[index]};
                border : none; 
            }}
            QTreeView::branch:!has-children:has-siblings:adjoins-item {{
                border-image : url({base_path}/{self._branch_more[index]}.png) 0;
                image : url({base_path}/{self._branch_more[index]}.png) 0;
            }}
            QTreeView::branch:!has-children:!has-siblings:adjoins-item {{
                border-image : url({base_path}/{self._branch_end[index]}.png) 0;
            }}
            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings {{
                    border-image : none;
                    image : url({base_path}/{self._branch_closed[index]}.png);
            }}

            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings  {{
                    border-image : none;
                    image : url({base_path}/{self._branch_open[index]}.png);
            }}
            QSlider::groove:horizontal {{
                height : 10px;
                margin-right : 10px;
                margin-left : 10px;
                background : {self._button_color[index]}; 
                border-radius : 5px;
            }}
            QSlider::handle:horizontal {{
                background : {self._slider_handle_color[index]};
                border : 1px solid {self._slider_handle_border[index]};
                width : 12px;
                margin-top : -3px 0;
                margin-right : -2px 0;
                margin-bottom : -2px 0;
                margin-left : -3px 0;
                border-radius : 7px;
            }}
            QSlider::handle:horizontal:disabled {{
                background : {self._slider_handle_color_disabled[index]};
            }}
            QSlider::handle:horizontal:hover {{
                background : {self._slider_handle_color_pressed[index]};
            }}
            QSlider::handle:horizontal:pressed {{
                background : {self._slider_handle_color_pressed[index]};
            }}
            QSwitchControl:unchecked{{
                background : {self._switch_off[index]};
            }}
            QSwitchControl:unchecked:disabled{{
                background : {self._switch_disabled[index]};
            }}
            QSwitchControl:checked{{
                background : {self._switch_on[index]};
            }}
            QSwitchControl:checked:disabled{{
                background : {self._switch_disabled[index]};
            }}
            QSwitchControl[type="switch"]::indicator, QSwitchControl[type="switch"]::indicator:disabled, QSwitchControl[important="False"]::indicator, QSwitchControl[important="False"]::indicator:disabled{{
                border : none;
                background : transparent;
                color : transparent;
            }}
            #theme_toggle:unchecked{{
                background : {self._switch_on[1]};
            }}
            #theme_toggle:checked{{
                background : {self._switch_on[0]};
            }}
            #light_mode {{
                image : url({base_path}/{self._light_mode[index]});
            }}
            #dark_mode {{
                image : url({base_path}/{self._dark_mode[index]});
            }}
            #info {{
                image : url({base_path}/{self._info[index]});
                background : transparent;
                color : transparent;
                border : none;
                border-radius : 12px;
            }}
            QSplitter::handle {{
                background : {self._frame_color[index]};
            }}
            #settings_button{{
                border : none;
                background : transparent;
                color : transparent;
                image : url({base_path}/{self._settings[index]});
            }}
            #help_button{{
                border : none;
                background : transparent;
                color : transparent;
                image : url({base_path}/{self._info[index]});
            }}
            #color{{
                border : 1px solid {self._color[index]};
            }}
            QToolTip {{
                border : 2px solid {self._menu_border[index]};;
                background : {self._frame_color[index]}; 
                color : {self._color[index]}; 
            }}
            """
        return style