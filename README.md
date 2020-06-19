sublime_plugin(http://www.sublimetext.cn/docs/3/api_reference.html)
====================

插件扩展API参考
一般信息
示例插件
插件生命周期
多线程
单位和坐标
类型
核心组件
sublime 模块
Sheet 类
View 类
Selection 类
Region 类
Phantom 类
PhantomSet 类
Edit 类
Window 类
Settings 类
插件扩展
sublime_plugin 模块
EventListener 类
ViewEventListener 类
ApplicationCommand 类
WindowCommand 类
TextCommand 类
TextInputHandler 类
ListInputHandler 类
一般信息
示例插件
------------
在Sublime Text 2中附带一些默认插件，可以在Default包中找到它们：

Packages/Default/delete_word.py删除光标左侧或右侧的单词
Packages/Default/duplicate_line.py复制当前行
Packages/Default/exec.py使用幻像显示内联错误
Packages/Default/font.py显示如何使用设置
Packages/Default/goto_line.py提示用户输入，然后更新选择
Packages/Default/mark.py使用add_regions()将图标添加到装订线
Packages/Default/show_scope_name.py使用弹出窗口显示插入符号的范围名称
Packages/Default/trim_trailing_whitespace.py在保存之前修改缓冲区
Packages/Default/arithmetic.py通过命令选项板运行时接受来自用户的输入
插件生命周期
------------
在导入时，插件可能不会调用任何API函数，但sublime.version()，sublime.platform()，sublime.architecture()和sublime.channel()除外。

如果插件定义了模块级函数plugin_loaded()，那么当API准备好使用时将调用它。插件也可以定义plugin_unloaded()，以便在插件卸载之前得到通知。

多线程
------------
所有API函数都是线程安全的，但请记住，从在备用线程中运行的代码的角度来看，应用程序状态将在代码运行时发生变化。

单位和坐标
------------
接受或返回坐标或尺寸的API函数使用与设备无关的像素(倾角)值来实现。虽然在某些情况下这些将等同于设备像素，但通常情况并非如此。根据CSS规范，minihtml将px单元视为与设备无关。

类型
------------
本文档通常仅涉及Python数据类型。某些类型名称是此处记录的类，但是也有一些自定义类型名称引用具有特定语义的构造：

location：元组(str，str，(int，int)，包含有关符号位置的信息。第一个字符串是绝对文件路径，第二个字符串是相对于项目的文件路径，第三个元素是行和列的双元素元组。
point：一个 int，表示从编辑器缓冲区开始的偏移量。的view方法 text_point()和 rowcol()允许转换和从这种格式。
value：任何Python数据类型 bool， int， float， str， list或 dict。
dip：表示与设备无关的像素的浮点数。
vector：表示 x和 y坐标的(dip，dip)元组。
CommandInputHandler： TextInputHandler或 ListInputHandler的子类。


sublime 模块
------------
方法	返回值	描述
set_timeout(callback, delay)	None	在给定的delay(以毫秒为单位)后 运行主线程中的callback。具有相等延迟的回调将按照添加的顺序运行。
set_timeout_async(callback, delay)	None	在给定的delay(以毫秒为单位)后在备用线程上 运行callback。
error_message(string)	None	向用户显示错误对话框。
message_dialog(string)	None	向用户显示消息对话框。
ok_cancel_dialog(string, <ok_title>)	bool	向用户显示确定/取消问题对话框。如果提供了ok_title，则可以将其用作ok按钮上的文本。如果用户按下ok按钮，则返回True。
yes_no_cancel_dialog(string, <yes_title>, <no_title>)	int	向用户显示是/否/取消问题对话框。如果提供yes_title和/或no_title，它们将用作某些平台上相应按钮上的文本。返回sublime.DIALOG_YES，sublime.DIALOG_NO或sublime.DIALOG_CANCEL。
load_resource(name)	str	加载给定的资源。该name应该是格式Packages/Default/Main.sublime-menu。
load_binary_resource(name)	bytes	加载给定的资源。该name应该是格式Packages/Default/Main.sublime-menu。
find_resources(pattern)	[str]	查找文件名与给定pattern匹配的资源。
encode_value(value, <pretty>)	str	将JSON兼容value编码为字符串表示形式。如果pretty设置为True，则字符串将包含换行符和缩进。
decode_value(string)	value	将JSON字符串解码为对象。如果string无效，则抛出ValueError。
expand_variables(value, variables)	value	使用字典变量中定义的变量 扩展字符串value中的所有variables。value也可以是list或dict，在这种情况下，结构将被递归扩展。字符串应使用片段语法，例如：expand_variables("Hello, ${name}", {"name": "Foo"})
load_settings(base_name)	Settings	加载命名设置。名称应包含文件名和扩展名，但不包括路径。将搜索包以查找与base_name匹配的文件，并将结果整理到设置对象中。随后调用load_settings()与BASE_NAME将返回相同的对象，而不是再次从磁盘加载设置。
save_settings(base_name)	None	将指定设置对象的任何内存中更改刷新到磁盘。
windows()	[Window]	返回所有打开窗口的列表。
active_window()	Window	返回最近使用的窗口。
packages_path()	str	返回所有用户的松散包所在的路径。
installed_packages_path()	str	返回所有用户的.sublime-package文件所在的路径。
cache_path()	str	返回Sublime Text存储缓存文件的路径。
get_clipboard(<size_limit>)	str	返回剪贴板的内容。size_limit用于防止不必要的大数据，默认为16,777,216个字符
set_clipboard(string)	None	设置剪贴板的内容。
score_selector(scope, selector)	int	将selector与给定scope匹配，返回分数。得分为0表示不匹配，高于0表示匹配。可以将不同的选择器与相同的范围进行比较：较高的分数意味着选择器是范围的更好匹配。
run_command(string, <args>)	None	使用(可选)给定的args 运行命名的ApplicationCommand。
get_macro()	[dict]	返回危害当前录制的宏的命令和参数列表。每个dict都包含keys 命令和args。
log_commands(flag)	None	控制命令记录。如果启用，则所有命令都从键绑定运行，菜单将记录到控制台。
log_input(flag)	None	控制输入​​记录。如果启用，则所有按键都将记录到控制台。
log_result_regex(flag)	None	控制结果正则表达式日志记录。这对于调试构建系统中使用的正则表达式很有用。
version()	str	返回版本号
platform()	str	返回平台，可能是"osx"，"linux"或"windows"
arch()	str	返回CPU架构，可能是"x32"或"x64"


sublime.Sheet 类
------------
表示窗口内的内容容器，即选项卡。表格可能包含视图或图像预览。
窗口或无查看或无
方法	返回值	描述
id()	int	返回唯一标识此工作表的数字。
window()		返回包含工作表的窗口。如果工作表已关闭，则可以为“ 无 ”。
view()		返回工作表中包含的视图。如果工作表是图像预览，或者视图已关闭，则可以为“ 无”。


sublime.View 类
------------
表示文本缓冲区的视图。请注意，多个视图可能引用相同的缓冲区，但它们有自己唯一的选择和几何。

方法	返回值	描述
id()	int	返回唯一标识此视图的数字。
buffer_id()	int	返回唯一标识此视图下的缓冲区的数字。
is_primary()	bool	如果视图是文件的主视图。如果用户已在文件中打开多个视图，则仅为False。
file_name()	str	全名文件是与缓冲区关联的文件，如果磁盘上不存在则为None。
name()	str	分配给缓冲区的名称(如果有)
set_name(name)	None	为缓冲区指定名称
is_loading()	bool	如果缓冲区仍在从磁盘加载，并且尚未准备好使用，则 返回True。
is_dirty()	bool	如果对缓冲区有任何未保存的修改，则 返回True。
is_read_only()	bool	如果可能未修改缓冲区，则 返回True。
set_read_only(value)	None	设置缓冲区的只读属性。
is_scratch()	bool	如果缓冲区是临时缓冲区，则 返回True。划痕缓冲区从不报告为脏。
set_scratch(value)	None	设置缓冲区的scratch属性。
settings()	Settings	返回对视图的设置对象的引用。对此设置对象的任何更改都将对此视图是私有的。
window()	Window	返回对包含视图的窗口的引用。
run_command(string, <args>)	None	使用(可选)给定的args 运行命名的TextCommand。
size()	int	返回文件中的字符数。
substr(region)	str	以字符串形式 返回region的内容。
substr(point)	str	返回该point右侧的字符。
insert(edit, point, string)	int	将给定string插入指定point的缓冲区中。返回插入的字符数：如果将制表符转换为当前缓冲区中的空格，则可能会有所不同。
erase(edit, region)	None	从缓冲区中 删除该region的内容。
replace(edit, region, string)	None	用给定的string 替换region的内容。
sel()	Selection	返回对选择的引用。
line(point)	Region	返回包含该point的行。
line(region)	Region	返回region的修改副本，使其从一行的开头开始，到一行的结尾。请注意，它可能跨越几行。
full_line(point)	Region	作为line()，但该区域包含尾随换行符，如果有的话。
full_line(region)	Region	作为line()，但该区域包含尾随换行符，如果有的话。
lines(region)	[Region]	返回与region相交的行列表(按排序顺序)。
split_by_newlines(region)	[Region]	将region拆分为使得返回的每个区域仅存在于一条线上。
word(point)	Region	返回包含该point的单词。
word(region)	Region	返回region的修改副本，使其从单词的开头开始，到单词结尾处结束。请注意，它可能会跨越几个单词。
classify(point)	int	
对point进行分类，返回零或多个这些标志的按位OR：

sublime.CLASS_WORD_START
sublime.CLASS_WORD_END
sublime.CLASS_PUNCTUATION_START
sublime.CLASS_PUNCTUATION_END
sublime.CLASS_SUB_WORD_START
sublime.CLASS_SUB_WORD_END
sublime.CLASS_LINE_START
sublime.CLASS_LINE_END
sublime.CLASS_EMPTY_LINE
find_by_class(point, forward, classes, <separators>)	Region	查找与给定class匹配的point之后的下一个位置。如果forward为False，则向后搜索而不是向前搜索。classes是sublime.CLASS_XXX标志的按位OR 。可以传入separators，以定义应该考虑哪些字符来分隔单词。
expand_by_class(point, classes, <separators>)	Region	将point向左和向右扩展，直到每一侧都落在与class匹配的位置。classes是sublime.CLASS_XXX标志的按位OR 。可以传入分隔符，以定义应该考虑哪些字符来分隔单词。
expand_by_class(region, classes, <separators>)	Region	向左和向右 扩展region，直到每一侧都落在与class匹配的位置。classes是sublime.CLASS_XXX标志的按位OR 。可以传入separators，以定义应该考虑哪些字符来分隔单词。
find(pattern, start_point, <flags>)	Region	返回匹配正则表达式模式的第一个区域，从start_point开始，如果找不到则返回None。可选的flags参数可以是sublime.LITERAL，sublime.IGNORECASE，也可以是两个ORed在一起。
find_all(pattern, <flags>, <format>, <extractions>)	[Region]	返回与正则表达式模式匹配的所有(非重叠)区域。可选的flags参数可以是sublime.LITERAL，sublime.IGNORECASE，也可以是两个ORed在一起。如果给出了格式字符串，则所有匹配项将使用格式化字符串进行格式化并放入提取列表中。
rowcol(point)	(int, int)	计算的基于0的行号和列号point。
text_point(row, col)	int	计算给定的基于0的row和col的字符偏移量。请注意，col被解释为超过行开头的字符数。
set_syntax_file(syntax_file)	None	更改视图使用的语法。syntax_file应该是Packages/Python/Python.tmLanguage的名称。要检索当前语法，请使用view.settings().get('syntax')。
extract_scope(point)	Region	返回在给定point分配给字符的语法范围名称的范围。
scope_name(point)	str	返回在给定point分配给字符的语法范围名称。
match_selector(point, selector)	bool	检查selector是否在给定point的范围内，如果匹配则返回bool。
score_selector(point, selector)	int	将selector与给定point的范围匹配，返回分数。得分为0表示不匹配，高于0表示匹配。可以将不同的选择器与相同的范围进行比较：较高的分数意味着选择器是范围的更好匹配。
find_by_selector(selector)	[Region]	查找与给定selector匹配的文件中的所有区域，并将它们作为列表返回。
show(location, <show_surrounds>)	None	滚动视图以显示给定location，该location可以是point，Region或Selection。
show_at_center(location)	None	将视图滚动到中心location，该location可以是point或Selection。
visible_region()	Region	返回视图的当前可见区域。
viewport_position()	vector	返回视口在布局坐标中的偏移量。
set_viewport_position(vector, <animate<)	None	将视口滚动到给定的布局位置。
viewport_extent()	vector	返回视口的宽度和高度。
layout_extent()	vector	返回布局的宽度和高度。
text_to_layout(point)	vector	将文本点转换为布局位置
text_to_window(point)	vector	将文本点转换为窗口位置
layout_to_text(vector)	point	将布局位置转换为文本点
layout_to_window(vector)	vector	将布局位置转换为窗口位置
window_to_layout(vector)	vector	将窗口位置转换为布局位置
window_to_text(vector)	point	将窗口位置转换为文本点
line_height()	dip	返回布局中使用的灯光高度
em_width()	dip	返回布局中使用的典型字符宽度
add_regions(key, [regions], <scope>, <icon>, <flags>)	None	
向视图 添加一组region。如果已存在具有给定key的一组region，则它们将被覆盖。的scope被用于源颜色来绘制region中，它应该是一个范围的名称，如"comment"或"string"。如果scope为空，则不会绘制region。

可选的图标名称(如果给定)将在每个区域旁边的装订线中绘制命名图标。该icon将使用与示波器关联的颜色进行着色。有效的图标名称是point，circle和bookmark。图标名称也可以是完整的包相对路径，例如Packages/Theme - Default/dot.png。

可选的flags参数是按位组合：

sublime.DRAW_EMPTY：使用垂直条绘制空白区域。默认情况下，它们根本不会被绘制。
sublime.HIDE_ON_MINIMAP：不显示小地图上的区域。
sublime.DRAW_EMPTY_AS_OVERWRITE：使用水平条而不是垂直条绘制空区域。
sublime.DRAW_NO_FILL：禁用填充区域，只留下轮廓。
sublime.DRAW_NO_OUTLINE：禁用绘制区域的轮廓。
sublime.DRAW_SOLID_UNDERLINE：在区域下方绘制一个实线下划线。
sublime.DRAW_STIPPLED_UNDERLINE：在区域下方绘制一个点状下划线。
sublime.DRAW_SQUIGGLY_UNDERLINE：在区域下方绘制一条波浪形下划线。
sublime.PERSISTENT：保存会话中的区域。
sublime.HIDDEN：不要绘制区域。
下划线样式是独占的，无论是零还是其中一个都应该给出。如果使用下划线，通常应传入sublime.DRAW_NO_FILL和sublime.DRAW_NO_OUTLINE。

get_regions(key)	[Region]	返回与给定key关联的区域(如果有)
erase_regions(key)	None	删除了指定的区域
set_status(key, value)	None	将状态key添加到视图。该value将显示在状态栏中，以逗号分隔的所有状态值列表，按键排序。将value设置为空字符串将清除状态。
get_status(key)	str	返回与key关联的先前分配的值(如果有)。
erase_status(key)	None	清除指定的状态。
command_history(index, <modifying_only>)	(str, dict, int)	
返回存储在undo/redo堆栈中的给定历史记录条目的命令名称，命令参数和重复计数。

索引0对应于最近的命令，-1对应于此之前的命令，依此类推。索引的正值表示在重做堆栈中查找命令。如果撤消/重做历史记录扩展得不够远，则返回(None，None，0)。

将modification_only设置为True(默认值为False)将仅返回修改缓冲区的条目。

change_count()	int	返回当前更改计数。每次修改缓冲区时，更改计数都会递增。更改计数可用于确定缓冲区自上次检查后是否已更改。
fold([regions])	bool	折叠给定region，如果它们已经折叠则 返回False
fold(region)	bool	折叠给定region，如果已经折叠则 返回False
unfold(region)	[Region]	展现在所有文本region，返回展开区域
unfold([regions])	[Region]	展现在所有文本region，返回展开区域
encoding()	str	返回当前与文件关联的编码
set_encoding(encoding)	None	对文件应用新编码。下次保存文件时将使用此编码。
line_endings()	str	返回当前文件使用的行结尾。
set_line_endings(line_endings)	None	设置下次保存时将应用的行结尾。
overwrite_status()	bool	返回覆盖状态，用户通常通过插入键切换。
set_overwrite_status(enabled)	None	设置覆盖状态。
symbols()	[(Region, str)]	提取缓冲区中定义的所有符号。
show_popup_menu(items, on_done, <flags>)	None	
在插入符号处显示弹出菜单，以选择列表中的项目。on_done将使用所选项的索引调用一次。如果取消弹出菜单，将使用参数-1调用on_done。

items是一个字符串列表。

flags它当前未使用。

show_popup(content, <flags>, <location>, <max_width>, <max_height>, <on_navigate>, <on_hide>)	None	
显示显示HTML内容的弹出窗口。

flags是以下的按位组合：

sublime.COOPERATE_WITH_AUTO_COMPLETE。使弹出窗口显示在自动完成菜单旁边
sublime.HIDE_ON_MOUSE_MOVE。移动，单击或滚动鼠标时弹出窗口隐藏
sublime.HIDE_ON_MOUSE_MOVE_AWAY。移动鼠标时弹出窗口(除非弹出窗口)或单击或滚动时弹出窗口
默认location的-1将显示在光标处弹出，否则文本点应该传递。

max_width和max_height设置弹出窗口的最大尺寸，之后将显示滚动条。

on_navigate是一个回调函数，它应该接受用户单击的链接上的href属性的字符串内容。

隐藏弹出窗口时调用on_hide。

update_popup(content)	None	更新当前可见弹出窗口的内容。
is_popup_visible()	bool	如果当前显示弹出窗口，则返回。
hide_popup()	None	隐藏弹出窗口。
is_auto_complete_visible()	bool	如果自动完成菜单当前可见，则返回。
style()	dict	返回视图的全局样式设置的dict。所有颜色都标准化为带有前导散列的六字符十六进制形式，例如＃ff0000。
style_for_scope(scope_name)	dict	接受字符串作用域名称并返回样式信息的dict，包括键foreground，bold，italic，source_line，source_column和source_file。如果范围具有背景颜色集，则将显示关键background。前景色和背景色被标准化为具有前导散列的六字符十六进制形式，例如＃ff0000。


sublime.Selection 类
------------
维护一组区域，确保没有重叠。区域按排序顺序保存。

方法	返回值	描述
clear()	None	删除所有区域。
add(region)	None	添加给定region。它将与集合中已包含的任何相交区域合并。
add_all(regions)	None	添加给定list或元组中的所有区域。
subtract(region)	None	从集合中的所有区域中 减去该region。
contains(region)	bool	如果给定region是子集，则 返回True。


sublime.Region 类
------------
表示缓冲区的一个区域。空区域，哪里a == b有效。

创建具有初始值a和b的Region。
构造函数	描述
Region(a, b)	
属性	类型	描述
a	int	该地区的第一个结束。
b	int	该地区的第二个目的地。可能少于a，在这种情况下该区域是反向的。
xpos	int	区域的目标水平位置，如果未定义，则为-1。按向上或向下键时的效果行为。
方法	返回值	描述
begin()	int	返回a和b的最小值。
end()	int	返回a和b的最大值。
size()	int	返回该区域跨越的字符数。始终> = 0。
empty()	bool	返回True iff begin() == end()。
cover(region)	Region	返回跨越此区域和给定区域的区域。
intersection(region)	Region	返回两个区域的集合交集。
intersects(region)	bool	返回True如果self == region或两者都包含一个或多个共同的位置。
contains(region)	bool	如果给定region是子集，则 返回True。
contains(point)	bool	返回True iff begin() <= point <= end()。


sublime.Phantom 类
------------
表示基于HTML的装饰，用于显示散布在视图中的不可编辑内容。与PhantomSet一起使用，可以将幻像实际添加到View中。构建Phantom并将其添加到View后，对属性的更改将不起作用。

创建附加到region的幻像。的content是HTML由被处理minihtml。

layout必须是以下之一：

sublime.LAYOUT_INLINE：显示region和后续点之间的幻像。
sublime.LAYOUT_BELOW：显示当前行下方空间中的幻像，与该region左对齐。
sublime.LAYOUT_BLOCK：显示当前行下方空间中的幻像，与行的开头左对齐。
on_navigate是一个可选的回调函数，它应该接受单个字符串参数，即单击链接的href属性。

构造函数	描述
Phantom(region, content, layout, <on_navigate>)	


sublime.PhantomSet 类
------------
一个管理虚位的集合，以及添加它们，更新它们并从视图中删除它们的过程。

创建附加到view的PhantomSet 。key是一个将Phantom组合在一起的字符串。
构造函数	描述
PhantomSet(view, <key>)	
方法	返回值	描述
update(phantoms)	None	
phantoms应该是一个虚位列表。

将更新集合中每个现有虚位的.region属性。将在视图中添加新的幻像，并且将删除不在phantoms列表中的幻像。


sublime.Edit 类
------------
编辑对象没有任何功能，它们存在于组缓冲区修改中。

编辑对象将传递给TextCommand，并且无法由用户创建。使用无效的Edit对象或来自不同View的Edit对象将导致需要它们的函数失败。

方法	返回值	描述
(no methods)		


sublime.Window 类
------------
查看或无
方法	返回值	描述
id()	int	返回唯一标识此窗口的数字。
new_file()	View	创建一个新文件。返回的视图将为空，其is_loaded()方法将返回True。
open_file(file_name, <flags>)	View	
打开指定的文件，并返回相应的视图。如果文件已经打开，它将被带到前面。注意，文件的加载是异步的，在返回的视图操作将是不可能的，直到它的is_loading()方法返回假。

可选的flags参数是按位组合：

sublime.ENCODED_POSITION：表示应搜索file_name ：row或：row：col后缀
sublime.TRANSIENT：仅作为预览打开文件：在修改之前，它不会分配标签
find_open_file(file_name)	View	在打开文件列表中查找指定文件，并返回相应的视图，如果没有打开此类文件则返回None。
active_sheet()	Sheet	返回当前关注的工作表。
active_view()	View	返回当前编辑的视图。
active_sheet_in_group(group)	Sheet	返回给定group中当前聚焦的工作表。
active_view_in_group(group)	View	返回给定group中当前编辑的视图。
sheets()	[Sheet]	返回窗口中所有打开的工作表。
sheets_in_group(group)	[Sheet]	返回给定group中的所有打开的工作表。
views()	[View]	返回窗口中的所有打开视图。
views_in_group(group)	[View]	返回给定group中的所有打开视图。
num_groups()	int	返回窗口中的视图组数。
active_group()	int	返回当前所选组的索引。
focus_group(group)	None	使给定group处于活动状态。
focus_sheet(sheet)	None	切换到给定的工作sheet。
focus_view(view)	None	切换到给定view。
get_sheet_index(sheet)	(int, int)	返回该组的内的组，和索引sheet。如果未找到，则返回-1。
set_sheet_index(sheet, group, index)	None	将工作sheet移动到给定的group和index。
get_view_index(view)	(int, int)	返回view组内的组和索引。如果未找到，则返回-1。
set_view_index(view, group, index)	None	将view移动到给定的group和索引。
status_message(string)	None	在状态栏中显示消息。
is_menu_visible()	bool	如果菜单可见，则 返回True。
set_menu_visible(flag)	None	控制菜单是否可见。
is_sidebar_visible()	bool	如果内容可用时将显示侧栏，则 返回True。
set_sidebar_visible(flag)	None	设置内容可用时要显示或隐藏的侧边栏。
get_tabs_visible()	bool	如果将显示打开文件的选项卡，则 返回True。
set_tabs_visible(flag)	None	控制是否显示打开文件的选项卡。
is_minimap_visible()	bool	如果启用了小地图，则 返回True。
set_minimap_visible(flag)	None	控制小地图的可见性。
is_status_bar_visible()	bool	如果将显示状态栏，则 返回True。
set_status_bar_visible(flag)	None	控制状态栏的可见性。
folders()	[str]	返回当前打开的文件夹列表。
project_file_name()	str	返回当前打开的项目文件的名称(如果有)。
project_data()	dict	返回与当前窗口关联的项目数据。数据的格式与.sublime-project文件的内容相同。
set_project_data(data)	None	更新与当前窗口关联的项目数据。如果窗口与.sublime-project文件关联，则项目文件将在磁盘上更新，否则窗口将在内部存储数据。
run_command(string, <args>)	None	使用(可选)给定的args 运行命名的WindowCommand。此方法能够运行任何类型的命令，通过输入焦点调度命令。
show_quick_panel(items, on_done, <flags>, <selected_index>, <on_highlighted>)	None	
显示快速面板，以选择列表中的项目。on_done将使用所选项的索引调用一次。如果快速面板被取消，将使用参数-1调用on_done。

items可以是字符串列表，也可以是字符串列表列表。在后一种情况下，快捷面板中的每个条目都将显示多行。

flags是sublime.MONOSPACE_FONT和sublime.KEEP_OPEN_ON_FOCUS_LOST的按位OR。

on_highlighted，如果给定，将在每次更改快速面板中突出显示的项目时调用。

show_input_panel(caption, initial_text, on_done, on_change, on_cancel)	View	显示输入面板，以从用户收集一行输入。on_done和on_change，如果不是None，都应该是期望单个字符串参数的函数。on_cancel应该是一个不需要参数的函数。返回用于输入窗口小部件的视图。
create_output_panel(name, <unlisted>)	View	
返回与命名输出面板关联的视图，并根据需要创建它。可以通过运行show_panel窗口命令来显示输出面板，并将panel参数设置为带有"output"的名称。字首。

可选的未列出参数是一个布尔值，用于控制是否应在面板切换器中列出输出面板。

find_output_panel(name)		返回与命名输出面板关联的视图，如果输出面板不存在，则返回None。
destroy_output_panel(name)	None	销毁命名的输出面板，如果当前打开则将其隐藏。
active_panel()	str or None	返回当前打开的面板的名称，如果没有打开面板，则返回None。除输出面板外，还将返回内置面板名称(例如"console"，"find"等)。
panels()	[str]	返回尚未标记为未列出的所有面板的名称列表。除输出面板外，还包括某些内置面板。
lookup_symbol_in_index(symbol)	[location]	返回在当前项目中的文件之间定义符号的所有位置。
lookup_symbol_in_open_files(symbol)	[location]	返回跨打开文件定义符号的所有位置。
extract_variables()	dict	
返回使用上下文键填充的字符串字典：

包，平台，文件，file_path，file_name，file_base_name，file_extension，文件夹，项目，project_path，project_name，project_base_name，project_extension。此dict适合传递给sublime.expand_variables()。


sublime.Settings 类
------------
方法	返回值	描述
get(name, <default>)	value	返回命名设置，如果未定义，则返回默认值。如果未通过，则默认值为None。
set(name, value)	None	设置命名设置。只接受原始类型，列表和dicts。
erase(name)	None	删除命名设置。不会从任何父设置中删除它。
has(name)	bool	如果此设置集或其父项之一中存在命名选项，则 返回True。
add_on_change(key, on_change)	None	只要更改此对象中的设置，就注册要运行的回调。
clear_on_change(key)	None	删除使用给定密钥注册的所有回调。


sublime_plugin 模块
------------
方法	返回值	描述
(no methods)		

sublime_plugin.EventListener 类
------------
请注意，其中许多事件都是由视图底层的缓冲区触发的，因此该方法只调用一次，第一个视图作为参数。

方法	返回值	描述
on_new(view)	None	在创建新缓冲区时调用。
on_new_async(view)	None	在创建新缓冲区时调用。在单独的线程中运行，不会阻止应用程序。
on_clone(view)	None	从现有视图克隆视图时调用。
on_clone_async(view)	None	从现有视图克隆视图时调用。在单独的线程中运行，不会阻止应用程序。
on_load(view)	None	文件加载完成后调用。
on_load_async(view)	None	文件加载完成后调用。在单独的线程中运行，不会阻止应用程序。
on_pre_close(view)	None	在视图即将关闭时调用。此时视图仍将在窗口中。
on_close(view)	None	视图关闭时调用(注意，可能仍有其他视图进入同一缓冲区)。
on_pre_save(view)	None	在视图保存之前调用。
on_pre_save_async(view)	None	在视图保存之前调用。在单独的线程中运行，不会阻止应用程序。
on_post_save(view)	None	视图保存后调用。
on_post_save_async(view)	None	视图保存后调用。在单独的线程中运行，不会阻止应用程序。
on_modified(view)	None	在对视图进行更改后调用。
on_modified_async(view)	None	在对视图进行更改后调用。在单独的线程中运行，不会阻止应用程序。
on_selection_modified(view)	None	在视图中修改选择后调用。
on_selection_modified_async(view)	None	在视图中修改选择后调用。在单独的线程中运行，不会阻止应用程序。
on_activated(view)	None	当视图获得输入焦点时调用。
on_activated_async(view)	None	当视图获得输入焦点时调用。在单独的线程中运行，不会阻止应用程序。
on_deactivated(view)	None	视图丢失输入焦点时调用。
on_deactivated_async(view)	None	视图丢失输入焦点时调用。在单独的线程中运行，不会阻止应用程序。
on_hover(view, point, hover_zone)	None	
当用户的鼠标悬停在视图上一小段时间时调用。

point是鼠标位置视图中的最近点。根据hover_zone的值，鼠标实际上可能并不相邻：

sublime.HOVER_TEXT：当鼠标悬停在文本上时。
sublime.HOVER_GUTTER：当鼠标悬停在排水沟上方时。
sublime.HOVER_MARGIN：当鼠标悬停在一行右侧的空白处时。
on_query_context(view, key, operator, operand, match_all)	bool or None	
在确定触发与给定上下文密钥的密钥绑定时调用。如果插件知道如何响应上下文，它应返回True of False。如果上下文未知，则应返回None。

运营商是以下之一：

sublime.OP_EQUAL：上下文的值是否等于操作数？
sublime.OP_NOT_EQUAL：上下文的值是否不等于操作数？
sublime.OP_REGEX_MATCH：上下文的值是否与操作数中给出的正则表达式匹配？
sublime.OP_NOT_REGEX_MATCH：上下文的值是否与操作数中给出的正则表达式不匹配？
sublime.OP_REGEX_CONTAINS：上下文的值是否包含与操作数中给出的正则表达式匹配的子字符串？
sublime.OP_NOT_REGEX_CONTAINS：上下文的值是否包含与操作数中给出的正则表达式匹配的子字符串？
如果上下文与选择相关，则应使用match_all：每个选择是否必须匹配(match_all == True)，或者至少是一个匹配(match_all == False)？

on_query_completions(view, prefix, locations)	list, tuple or None	
每当完成将被呈现给用户时调用。该前缀是文本完成的unicode字符串。

location是一个点列表。由于无论语法如何view.match_selector(point, relevant_scope)都要为每个视图中的所有完成调用此方法，因此应调用此方法以确定该点是否相关。

返回值必须是以下格式之一：

无：未提供完成

return None
2元素列表/元组的列表。第一个元素是完成触发器的unicode字符串，第二个元素是unicode替换文本。

return [["me1", "method1()"], ["me2", "method2()"]]
触发器可能包含一个制表符(\t)，后跟一个提示，显示在完成框的右侧。

return [
    ["me1\tmethod", "method1()"],
    ["me2\tmethod", "method2()"]
]
替换文本可能包含美元数字字段，例如片段，例如$ 0，$ 1。

return [
    ["fn", "def ${1:name}($2) { $0 }"],
    ["for", "for ($1; $2; $3) { $0 }"]
]
一个2元素元组，第一个元素是上面列出的列表格式，第二个元素是以下列表中的位标志：

sublime.INHIBIT_WORD_COMPLETIONS：防止Sublime Text根据视图内容显示完成情况
sublime.INHIBIT_EXPLICIT_COMPLETIONS：防止Sublime Text显示基于.sublime-completions文件 的完成
return (
    [
        ["me1", "method1()"],
        ["me2", "method2()"]
    ],
    sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS
)
on_text_command(view, command_name, args)	(str, dict)	发出文本命令时调用。监听器可以返回一个(command, arguments)元组来重写命令，或者返回None来运行未修改的命令。
on_window_command(window, command_name, args)	(str, dict)	发出窗口命令时调用。监听器可以返回一个(command, arguments)元组来重写命令，或者返回None来运行未修改的命令。
on_post_text_command(view, command_name, args)	None	在执行文本命令后调用。
on_post_window_command(window, command_name, args)	None	在执行窗口命令后调用。


sublime_plugin.ViewEventListener 类
------------
一个类，它为EventListener提供类似的事件处理，但绑定到特定视图。提供基于类方法的过滤，以控制为其创建的视图对象。

视图作为单个参数传递给构造函数。默认实现通过self.view使视图可用。

分类方法	返回值	描述
is_applicable(settings)	bool	一个@classmethod接收一个设置对象和应返回布尔指示此类适用于使用这些设置的图
applies_to_primary_view_only()	bool	一个@classmethod应该返回一个布尔值，表示如果该类只适用于一个文件中的主视图。如果视图是文件的唯一视图或第一视图，则视图被视为主视图。
方法	返回值	描述
on_load()	None	文件加载完成后调用。
on_load_async()	None	文件加载完成后调用。在单独的线程中运行，不会阻止应用程序。
on_pre_close()	None	在视图即将关闭时调用。此时视图仍将在窗口中。
on_close()	None	视图关闭时调用(注意，可能仍有其他视图进入同一缓冲区)。
on_pre_save()	None	在视图保存之前调用。
on_pre_save_async()	None	在视图保存之前调用。在单独的线程中运行，不会阻止应用程序。
on_post_save()	None	视图保存后调用。
on_post_save_async()	None	视图保存后调用。在单独的线程中运行，不会阻止应用程序。
on_modified()	None	在对视图进行更改后调用。
on_modified_async()	None	在对视图进行更改后调用。在单独的线程中运行，不会阻止应用程序。
on_selection_modified()	None	在视图中修改选择后调用。
on_selection_modified_async()	None	在视图中修改选择后调用。在单独的线程中运行，不会阻止应用程序。
on_activated()	None	当视图获得输入焦点时调用。
on_activated_async()	None	当视图获得输入焦点时调用。在单独的线程中运行，不会阻止应用程序。
on_deactivated()	None	视图失去输入焦点时调用。
on_deactivated_async()	None	视图失去输入焦点时调用。在单独的线程中运行，不会阻止应用程序。
on_hover(point, hover_zone)	None	
当用户的鼠标在视图上盘旋一小段时间时调用。

point是鼠标位置视图中的最近点。根据hover_zone的值，鼠标实际上可能并不相邻：

sublime.HOVER_TEXT：当鼠标悬停在文本上时。
sublime.HOVER_GUTTER：当鼠标悬停在排水沟上方时。
sublime.HOVER_MARGIN：当鼠标悬停在一行右侧的空白处时。
on_query_context(key, operator, operand, match_all)	bool or None	
在确定触发与给定上下文密钥的密钥绑定时调用。如果插件知道如何响应上下文，它应返回True of False。如果上下文未知，则应返回None。

运营商是以下之一：

sublime.OP_EQUAL：上下文的值是否等于操作数？
sublime.OP_NOT_EQUAL：上下文的值是否不等于操作数？
sublime.OP_REGEX_MATCH：上下文的值是否与操作数中给出的正则表达式匹配？
sublime.OP_NOT_REGEX_MATCH：上下文的值是否与操作数中给出的正则表达式不匹配？
sublime.OP_REGEX_CONTAINS：上下文的值是否包含与操作数中给出的正则表达式匹配的子字符串？
sublime.OP_NOT_REGEX_CONTAINS：上下文的值是否包含与操作数中给出的正则表达式匹配的子字符串？
如果上下文与选择相关，则应使用match_all：每个选择是否必须匹配(match_all == True)，或者至少是一个匹配(match_all == False)？

on_query_completions(prefix, locations)	list, tuple or None	
每当完成将被呈现给用户时调用。该前缀是文本完成的unicode字符串。

location是一个点列表。由于无论语法如何self.view.match_selector(point, relevant_scope)都要为所有完成调用此方法，因此应调用此方法以确定该点是否相关。

返回值必须是以下格式之一：

无：未提供完成

return None
2元素列表/元组的列表。第一个元素是完成触发器的unicode字符串，第二个元素是unicode替换文本。

return [["me1", "method1()"], ["me2", "method2()"]]
触发器可能包含一个制表符(\ t)，后跟一个提示，显示在完成框的右侧。

return [
    ["me1\tmethod", "method1()"],
    ["me2\tmethod", "method2()"]
]
替换文本可能包含美元数字字段，例如片段，例如$ 0，$ 1。

return [
    ["fn", "def ${1:name}($2) { $0 }"],
    ["for", "for ($1; $2; $3) { $0 }"]
]
一个2元素元组，第一个元素是上面列出的列表格式，第二个元素是以下列表中的位标志：

sublime.INHIBIT_WORD_COMPLETIONS：防止Sublime Text根据视图内容显示完成情况
sublime.INHIBIT_EXPLICIT_COMPLETIONS：防止Sublime Text显示基于.sublime-completions文件 的完成
return (
    [
        ["me1", "method1()"],
        ["me2", "method2()"]
    ],
    sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS
)
on_text_command(command_name, args)	(str, dict)	发出文本命令时调用。监听器可以返回一个(command_name, args)元组来重写命令，或者返回None来运行未修改的命令。
on_post_text_command(command_name, args)	None	在执行文本命令后调用。


sublime_plugin.ApplicationCommand 类
------------
CommandInputHandler 或 None
方法	返回值	描述
run(<args>)	None	运行命令时调用。
is_enabled(<args>)	bool	如果此时能够运行该命令，则 返回True。默认实现总是返回True。
is_visible(<args>)	bool	如果此时命令应显示在菜单中，则 返回True。默认实现始终返回True。
is_checked(<args>)	bool	如果菜单项旁边应显示一个复选框，则 返回True。该.sublime菜单文件必须设置为复选框属性真正被用于此目的。
description(<args>)	str	返回具有给定参数的命令的描述。如果没有提供标题，则在菜单中使用。返回None以获取默认描述。
input(args)		如果返回None以外的其他内容，则会在命令选项板中运行命令之前提示用户输入。


sublime_plugin.WindowCommand类
------------
WindowCommands每个窗口实例化一次。可以通过self.window检索Window对象

CommandInputHandler 或 None
方法	返回值	描述
run(<args>)	None	运行命令时调用。
is_enabled(<args>)	bool	如果此时能够运行该命令，则 返回True。默认实现总是返回True。
is_visible(<args>)	bool	如果此时命令应显示在菜单中，则 返回True。默认实现始终返回True。
description(<args>)	str	返回具有给定参数的命令的描述。如果没有提供标题，则在菜单中使用。返回None以获取默认描述。
input(args)		如果返回None以外的其他内容，则会在命令选项板中运行命令之前提示用户输入。


sublime_plugin.TextCommand 类
------------
每个视图都会实例化一次TextCommands。可以通过self.view检索View对象

CommandInputHandler 或 None
方法	返回值	描述
run(edit, <args>)	None	运行命令时调用。
is_enabled(<args>)	bool	如果此时能够运行该命令，则 返回True。默认实现总是返回True。
is_visible(<args>)	bool	如果此时命令应显示在菜单中，则 返回True。默认实现始终返回True。
description(<args>)	str	返回具有给定参数的命令的描述。用于菜单和撤消/重做描述。返回None以获取默认描述。
want_event()	bool	返回True以在鼠标操作触发命令时接收事件参数。事件信息允许命令确定单击视图的哪个部分。默认实现返回False。
input(args)		如果返回None以外的其他内容，则会在命令选项板中运行命令之前提示用户输入。


sublime_plugin.TextInputHandler 类
------------
TextInputHandlers可用于接受命令选项板中的文本输入。从命令的input()方法返回this的子类。

CommandInputHandler 或 None
方法	返回值	描述
name()	str	此输入处理程序正在编辑的命令参数名称。对于名为FooBarInputHandler的输入处理程序，默认为foo_bar
placeholder()	str	在用户输入任何内容之前，占位符文本显示在文本输入框中。默认为空。
initial_text()	str	文本输入框中显示的初始文本。默认为空。
preview(text)	str or sublime.Html(str)	每当用户更改输入框中的文本时调用。返回值(纯文本或HTML)将显示在命令选项板的预览区域中。
validate(text)	bool	每当用户在文本输入框中按Enter键时调用。返回False以禁止当前值。
cancel()	None	当取消输入处理程序时，用户按退格键或退出时调用。
confirm(text)	None	在接受输入时调用，在用户按下回车并且文本已经过验证之后。
next_input(args)		用户完成此输入后返回下一个输入。可以返回None表示不再需要输入，或者返回sublime_plugin.BackInputHandler()以指示输入处理程序应该从堆栈中取出。
description(text)	str	当此输入处理程序不在输入处理程序堆栈顶部时，在Command Palette中显示的文本。默认为用户输入的文本。


sublime_plugin.ListInputHandler 类
------------
ListInputHandlers可用于接受命令选项板中列表项的选择输入。从命令的input()方法返回this的子类。

方法	返回值	描述
name()	str	此输入处理程序正在编辑的命令参数名称。对于名为FooBarInputHandler的输入处理程序，默认为foo_bar
list_items()	[str] or [(str,value)]	要在列表中显示的项目。如果返回(str，value)元组的列表，则str将显示给用户，而该值将用作命令参数。
(可选)返回(list_items，selected_item_index)元组以指示初始选择。

placeholder()	str	在用户输入任何内容之前，占位符文本显示在文本输入框中。默认为空。
initial_text()	str	过滤器框中显示的初始文本。默认为空。
preview(value)	str or sublime.Html(str)	每当用户更改所选项目时调用。返回值(纯文本或HTML)将显示在命令选项板的预览区域中。
validate(value)	bool	每当用户在文本输入框中按Enter键时调用。返回False以禁止当前值。
cancel()	None	当取消输入处理程序时，用户按退格键或退出时调用。
confirm(value)	None	在接受输入时调用，在用户按下enter并且项目已经过验证后调用。
next_input(args)	CommandInputHandler or None	用户完成此输入后返回下一个输入。可以返回None表示不再需要输入，或者返回sublime_plugin.BackInputHandler()以指示输入处理程序应该从堆栈中取出。
description(value, text)	str	当此输入处理程序不在输入处理程序堆栈顶部时，在Command Palette中显示的文本。默认为用户选择的列表项的文本。
