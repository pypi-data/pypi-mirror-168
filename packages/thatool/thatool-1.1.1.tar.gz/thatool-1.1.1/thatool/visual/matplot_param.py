from cycler import cycler

### ============================================================================
### Matplot Parameter for Plot
### ============================================================================
## I. Use Runtime rc settings
""" This part contains some Global parameters to set for Matplotlib based on the way called "Setting rcParams at runtime". All rc settings are stored in a dictionary-like variable called `matplotlib.rcParams`, to see all valid Params:
	```python
		import matplotlib as mpl
		mpl.rcParams.keys()
	```

Examples:
	```python
		from thatool.visualize import matplot_param
		import matplotlib.pyplot as plt
		plt.rcParams.update(matplot_param.myPARAM)
	```

Refs:
	[1]. [Customizing Matplotlib with style sheets and rcParams](https://matplotlib.org/stable/tutorials/introductory/customizing.html#sphx-glr-tutorials-introductory-customizing-py)

fontsize for legend, stick,...not for text: fontsize : int or float or {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large', 'larger', 'smaller'}
'smaller'= 83%% of the current font size.
### use latex: https://matplotlib.org/stable/tutorials/text/usetex.html
font.family: 'san-serif' 'serif' or 'monospace'
### font family: https://tinyurl.com/ygestjxo
	- 'serif': Serifs are small decorative flourishes attached to stroke ends of characters. Fonts such as Times New Roman, Century, Garamond, and Palatino are serif fonts.
	- 'sans-serif': This means without serif. Fonts such as Helvetica, Arial, Calibri, and DejaVu Sans are sans-serif.
	- 'monospace': Monospace fonts have characters of the same width. They are usually used for code.
	- 'cursive': Cursive features connected brush strokes, usually in italic, that give a sense of classical elegance.
	- 'fantasy': Decorative fonts that look funny.
### Math mode: https://tinyurl.com/yjttcr2c
	#mathtext.fontset: dejavusans  # Should be 'dejavusans' (default), 'dejavuserif', 'cm' (Computer Modern), 'stix',
									# 'stixsans' or 'custom' (unsupported, may go away in the future)
	## "mathtext.fontset: 'custom" is defined by the mathtext.bf, .cal, .it, ...
	## settings which map a TeX font name to a fontconfig font pattern.  (These settings are not used for other font sets.)
	#mathtext.bf:  sans:bold
	#mathtext.cal: cursive
	#mathtext.it:  sans:italic
	#mathtext.rm:  sans
	#mathtext.sf:  sans
	#mathtext.tt:  monospace
	#mathtext.fallback: cm  # Select fallback font from ['cm' (Computer Modern), 'stix'
							# 'stixsans'] when a symbol can not be found in one of the
							# custom math fonts. Select 'None' to not perform fallback
							# and replace the missing character by a dummy symbol.
	#mathtext.default: it
"""

myCOLOR = ['black','red','blue','green','magenta','orange','lime','cyan','violet','purple','olive','gray','yellow','navy','saddlebrown','darkgreen','lawngreen', 'lightgreen','steelblue','darkcyan','plum','slateblue','indigo']

myPARAM = {                             # define a DICT
	### Set global font
	"font.family":'sans-serif', 'font.sans-serif':'Tahoma',              # 'sans-serif' family of Arial font: Arial, Tahoma, Courier New, Comic Sans MS,Segoe UI,Lucida Console
	# "font.family":'serif', 'font.serif': ['Times New Roman'],          # "serif" family of Times font: Times New Roman,

	### Math mode
	# 'text.usetex':True,                                                # use latex
	# 'mathtext.fontset':'custom', 'mathtext.sf':'sans',                    # use Mathtext

	### Set fontsize
	'font.size':10,
	'legend.fontsize':'smaller',
	'axes.labelsize': 'medium', 'axes.titlesize':'medium', "figure.titlesize":'larger',
	'xtick.labelsize':'medium', 'ytick.labelsize':'medium',
	### Change the appearance of ticks, tick labels, and gridlines: https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.axes.Axes.tick_params.html
	'axes.grid':True, 'axes.grid.axis':'both', 'axes.grid.which': 'major',
	'grid.linestyle': (5, 10), 'grid.linewidth':0.4, 'grid.color':'gray',           # 'grid.linestyle': (0, (5, 10))
	'xtick.direction':'in', 'xtick.major.size': 3.5, 'xtick.major.width': 0.7,
	'ytick.direction':'in', 'ytick.major.size': 3.5, 'ytick.major.width': 0.7,
	### Line & marker
	'lines.linewidth': 1,
	'lines.markersize': 4,
	### Legend
	'legend.frameon':True,
	### Figure size
	'figure.figsize': [3.375, 2.7], 'figure.dpi': 300,
	'savefig.dpi': 'figure', 'savefig.pad_inches': 0.05,

	### color
	'axes.prop_cycle': cycler('color', myCOLOR),

	}


## linestyle: https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
myLINE = {
     'solid': 'solid',      # Same as (0, ()) or '-'
     'dotted': 'dotted',    # Same as (0, (1, 1)) or ':'
     'dashed': 'dashed',    # Same as '--'
     'dashdot': 'dashdot',  # Same as '-.'

     'loosely dotted':        (0, (1, 10)),
     'dotted':                (0, (1, 1)),
     'densely dotted':        (0, (1, 1)),

     'loosely dashed':        (0, (5, 10)),
     'dashed':                (0, (5, 5)),
     'densely dashed':        (0, (5, 1)),

     'loosely dashdotted':    (0, (3, 10, 1, 10)),
     'dashdotted':            (0, (3, 5, 1, 5)),
     'densely dashdotted':    (0, (3, 1, 1, 1)),

     'dashdotdotted':         (0, (3, 5, 1, 5, 1, 5)),
     'loosely dashdotdotted': (0, (3, 10, 1, 10, 1, 10)),
     'densely dashdotdotted': (0, (3, 1, 1, 1, 1, 1))
	}

## marker: https://matplotlib.org/stable/gallery/lines_bars_and_markers/marker_reference.html
myMARKER = ['o','s','D','p','*','^','d','H','X','>','<','^']











