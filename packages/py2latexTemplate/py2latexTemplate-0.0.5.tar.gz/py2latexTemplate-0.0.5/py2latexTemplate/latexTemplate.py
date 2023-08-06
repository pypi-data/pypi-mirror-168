import sympy as sp
# from sympy.printing.latex import LatexPrinter #remove

import pickle
import re
import os

module_path = os.path.dirname(os.path.abspath(__file__))
cwd = os.getcwd()


from pathlib import Path
# Matrix
# print_latex
# latex

# % \begin{dmath*}[layout={L}], ?, D, L, S, l, A
# \eqpunct{,}
with open(os.path.join(module_path, 'OML.pickle'), 'rb') as p:
  OMLcode = pickle.load(p)

rel_symbols = []

with open(os.path.join(module_path, 'flexSymbols.pickle'), 'rb') as p:
  flex_symbols = pickle.load(p)
  
  for sym, info in flex_symbols.items():
    if not len(info): continue
    if info[0] == "Rel": rel_symbols.append(sym)


# latexPrinter = LatexPrinter()


def reset_sp_params():
  sp.core.parameters.global_parameters.__setattr__("evaluate", True)
  sp.core.parameters.global_parameters.__setattr__("distribute", True)
  sp.core.parameters.global_parameters.__setattr__("exp_is_pow", False)
  #
  # latexPrinter._settings['order'] = None #remove

def negcolast(expr):
  from sympy.core.function import _coeff_isneg
  if isinstance(expr, sp.Add) and _coeff_isneg(expr.args[0]):
    args = list(expr.args)
    args.append(args.pop(0))
    return sp.UnevaluatedExpr(sp.Add(*args, evaluate=False))
  else:
    return expr

def orderedPoly(poly):
  return poly.as_expr().replace(sp.Add, lambda *args: negcolast(sp.Add(*args)))


def sortByPow(expr, descending=True):
  sorted_args = list(sorted(expr.args, key=lambda e: max(e.as_powers_dict().values()), reverse=descending))

  new_expr = sp.UnevaluatedExpr(sp.Add(*sorted_args, evaluate=False))

  return new_expr

  
from sympy.core.parameters import evaluate

# import sp.core.parameters.evaluate
# def unevaluated(content):
#   with sp.core.parameters.evaluate(False):
     

class LatexCommands:
  # quad_ = sp.Symbol(r'\quad') #TODO: phase out `Latex.quad_` for `Latex._quad`
  # condition_ = sp.Symbol(r'\condition') #TODO: phase out `Latex.condition_` for `Latex._condition()`
  conditionpunct_ = sp.Symbol(r'\conditionpunct')
  conditionmath_ = sp.Symbol(r'\conditionmath')
  implies_ = sp.Symbol('\implies')
  Rightarrow_ = sp.Symbol('\Rightarrow')
  approxx_ = sp.Symbol(r'\approxx')
  coloneq_ = sp.Symbol(r'\coloneq')
  coloneqq_ = sp.Symbol(r'\coloneqq') #sp.Symbol(r':=')
  eqq_ = sp.Symbol(r'\eqq ')
  neq_ = sp.Symbol(r'\neq')
  leq_ = sp.Symbol(r'\leq')
  cmark_ = sp.Symbol(r'\cmark')
  xmark_ = sp.Symbol(r'\xmark')
  cdot_ = r'\cdot'
  # cdot_ = sp.Symbol(r'\cdot')
  minus_ = sp.Symbol(r'-')
  eq_ = sp.Symbol(r'=')
  times_ = sp.Symbol(r'\times')
  dots_ = sp.Symbol(r'\dots')
  vdots_ = sp.Symbol(r'\vdots')
  ddots_ = sp.Symbol(r'\ddots')
  #
  # _linebreak = sp.Symbol(r' \\')
  # _linebreak = sp.Symbol(r'\linebreak')
  _linebreak = r'\linebreak'
  _newpage = sp.Symbol(r'\newpage')
  _eqframe = '[frame]'
  _quad = sp.Symbol(r'\quad')

  sp_order = "none"
  sp_evaluate = True

  # _eqlabel = r'\label{eq:test}'
  #
  # custom_commands = []
  # rel_symbols.extend([coloneq_, coloneqq_, eq_])
  rel_symbols = rel_symbols.copy() + [coloneq_, coloneqq_, eq_]
  declared_symbols = []

  QandA_level = -1
  # 
  def _def(self, s, d):
    try:
      return sp.Symbol(r"\def\{s}".format(s=s) + "{" + sp.latex(sp.sympify(d), order=self.sp_order) + "}")
    except:
      return sp.Symbol(r"\def\{s}".format(s=s) + "{" + str(d) + "}")

  def _header(self, s, bold=True, underlined=False, italic=False):
    style_args = ''
    if bold: style_args += r'\bfseries'
    if underlined: style_args += r'\ulined'
    if italic: style_args += r'\itshape'
    if len(style_args): return sp.Symbol(r'\header[' + style_args + ']{' + s + '}')
    else: return sp.Symbol(r'\header{' + s + '}')

  def Det_(self, M):
    return sp.Symbol(r'\Det{' + sp.latex(M) + '}')

  def boxed_(self, eq):
    return sp.Symbol(r'\boxed{' + sp.latex(eq, order=self.sp_order) + '}')
  
  def _centerHeader(self, content):
    return sp.latex(sp.Symbol(r'\begin{center}{\Large \textbf{')) + content + sp.latex(sp.Symbol(r'}}\end{center}'))
  
  def _section(self, content):
    return sp.latex(sp.Symbol(r'\section*{' + content +'}'))

  def _displaySkip(self, vspace="2pt", indent=True):
    return r'\displaySkip' + (r'[\indent]{' if indent else '{') + str(vspace) + '}'

  def _itemizedDescription(self, items_dict, pre_description=None):
    output = '\\begin{description}\n'
    if pre_description is not None:
      if type(pre_description) == list: pre_description = formatSentence(pre_description)
      output += f'\\item {pre_description}\n'
    for item, desc in items_dict.items():
      if "sympy" in str(type(item)): item = '$' + sp.latex(item, order=self.sp_order) + '$'
      if type(desc) == list: desc = formatSentence(desc)
      output += f'\\item[\\hspace\\leftmargin{item}] {desc}\n'
    output += r'\end{description}'
    return output

  def symbol(self, s, commutative=False):
    return sp.Symbol(s, commutative=commutative)

  def _DeclareFlexSymbol(self, sym, math_class="Rel"):
    # math sym: Ord (ordinary), COs [sum like] COi [integral-like] (operators), Bin (binary), Rel (relation), Pun (punctuation), DeL (open), DeR (close), Var (variable)
    try:
      encoding = OMLcode[sym]
    except Exception:
      sym = sp.latex(sym)
      encoding = OMLcode[sym]

    if math_class == "Rel": self.rel_symbols.append(sym)

    self.declared_symbols.append(sym)

    return "\\DeclareFlexSymbol{" + sym + "}{" + math_class + "}{OML}{"+ encoding +"}"

  def resetSymbols(self, exclude=[]):
    output = []
    for sym in self.declared_symbols:
      if sym in exclude: continue
      else:
        self.declared_symbols.remove(sym)
        if sym in self.rel_symbols: self.rel_symbols.remove(sym)

      info = flex_symbols[sym]
      output.append("\\DeclareFlexSymbol{" + sym + "}" + "".join(["{" + x + "}" for x in info]))
    return output
    
  def _pltFig(self, pgf_path, caption=None):
    output = r'\begin{figure}[H]\begin{center}'
    output += r'\input{' + pgf_path + '}'
    output += r'\end{center}'
    if caption is not None: output += r'\caption{' + caption + '}'
    output += r'\end{figure}'
    return output
  
  def _table(self, content, header):
    output = []
    header = [r'\textbf{' + h + '}' for h in header]
    output.append(' & '.join(header)) # + r' \\ [0.5ex]')

    for row in content:
      row = [x if type(x) == str else '$' + sp.latex(x, order=self.sp_order) + '$' for x in row]
      output.append('&'.join(row))

    output.append(r'\end{tabular}')
    output = r'\begin{tabular}{|' + ('c |' * len(header)) + '} \hline' + r'\\ \hline '.join(output) + r' \\'

    return output

  def _beginQandA(self):
    self.QandA_level += 1
    return r'\begin{QandA}'

  def _endQandA(self):
    self.QandA_level -= 1
    return r'\end{QandA}'

  def _QandAitem(self, text='~'):
    nested_counter = ["i", "ii", "iii", "iv"]    
    label = ''.join([r'\theenum' + nested_counter[i] for i in range(self.QandA_level+1)])
    return r'\item ' + text + r' \label{' + label + '}'

  def _inlineEq(self, label, eq=None):
    if eq is None: return r'\inlineEq[eq:' + label + ']{}'
    else: return r'\inlineEq[eq:' + label + ']{' + (eq if type(eq) == str else sp.latex(eq, order=self.sp_order)) + '}' # [eq:inline]{a+1=b}

  def _condition(self, s):
    return r'\condition{' + formatSentence(s) + r'} \\'

  def _ref(self, ref):
    return r'\ref{' + ref + '}'

  def _eqref(self, ref):
    return r'\eqref{eq:' + ref + '}'

  def _codeBlock(self, code, language="python"):
    output = [r"\begin{minted}{" + language + "}"]
    output.extend(code)
    output.append(r"\end{minted}")
    return "\n".join(output)

  def isMathSymbol(self, s):
    syms = [x for x in self.__dir__() if x[0] != '_'] + ["=", ":=", "+", "-"]
    
    return str(s)[1:]+'_' in syms or str(s).strip() in syms

  def isLatexCommand(self, s):
    commands = [x for x in self.__dir__() if len(x) > 1 and x[0] == '_' and x[1] != '_']
    if r'\def' in str(s) or re.search(r'\\begin{(?!matrix)\w*', str(s)) or re.search(r'\\end{(?!matrix)\w*', str(s)) or r'\new' in str(s) or r'\renew' in str(s) or r'\section' in str(s) or r'\thispagestyle' in str(s): return True # r'\begin{center}'
    elif '{' in str(s):
      if '[' in str(s): return '_' + str(s)[1:str(s).index('[')] in commands
      else: return '_' + str(s)[1:str(s).index('{')] in commands
    else: return '_' + str(s)[1:] in commands
  
  def no_sep(self, s):
    syms = [self.implies_]
    return s in syms or type(s) == str # or r'\def' in str(s)

  def no_eval(self):
    self.sp_evaluate = False
    # sp_no_eval()
    sp.core.parameters.global_parameters.__setattr__("evaluate", False)

  def reset_eval(self):
    self.sp_evaluate = True
    sp.core.parameters.global_parameters.__setattr__("evaluate", True)
    # reset_sp_params()

  def negLast(self, expr):
    return expr.replace(sp.Add, lambda *args: negcolast(sp.Add(*args)))
  # def reset_sp_params(self):
  #   sp.core.parameters.global_parameters.__setattr__("evaluate", True)
  #   sp.core.parameters.global_parameters.__setattr__("distribute", True)
  #   sp.core.parameters.global_parameters.__setattr__("exp_is_pow", False)


Latex = LatexCommands() #TODO: make this the export instead


def formatEq(content, env="dmath"):
  with evaluate(Latex.sp_evaluate): #new #TODO: add to other spots
    if type(content) != tuple:
      if isinstance(content, sp.Poly): content = sortByPow(content.as_expr()) #new #*
      return sp.latex(content, order=Latex.sp_order) + r' \\'

    out = []

    sympy_eq = None #sp.Eq(content[0], content[1], evaluate=False)
    for i, eq in enumerate(content):
      if isinstance(eq, sp.Poly):
        eq = sortByPow(eq.as_expr())
        # eq = orderedPoly(eq)
        # print(sp.latex(eq, order='none')) #remove #debug
        # eq = eq.as_expr() #new #*

      if type(eq) == str or Latex.isMathSymbol(eq) or Latex.isLatexCommand(eq):
        if sympy_eq is not None: out.append(sp.latex(sympy_eq, order=Latex.sp_order))
        
        if eq == Latex.cdot_: out.append(r'\cdot') #weird formatting...
        elif Latex.isMathSymbol(eq): out.append(sp.latex(eq, order=Latex.sp_order))
        elif eq[0] == "$" and eq[-1] == "$": out.append(eq[1:-1])
        else: out.append(eq)

        sympy_eq = None

      elif i > 0 and content[i-1] == Latex.conditionmath_: out.append("{" + sp.latex(eq, order=Latex.sp_order) + "}")
      elif sympy_eq is None: sympy_eq = eq
      else: sympy_eq = sp.Eq(sympy_eq, eq, evaluate=False)
      
    if sympy_eq is not None: out.append(sp.latex(sympy_eq, order=Latex.sp_order))

    if (env == "dmath" or len(content) == 1) and out[-1] != Latex._quad and r"\condition" not in out[-1]: out.append(r' \\')
    # if (env == "dmath" or len(content) == 1) and out[-1] != Latex._quad: out.append(r' \\') # and r"\condition" not in out[-1] #go back! #?
    if env != "dmath": out = [ln.replace(" = ", r" \eqq ") for ln in out]

    return ' '.join(out)


def formatSentence(content, env=None):
  if type(content) != list: content = [content]
  out = []

  if env != "dmath": x = "$"
  else: x = ""

  for eq in content:
    if type(eq) == str: out.append(eq)
    elif type(eq) == tuple: out.append(x + formatEq(eq, env) + x)
    else: out.append(x + sp.latex(eq, order=Latex.sp_order) + x)

  return ''.join(out)


# \renewcommand*{\@eqnnum}{{\normalfont \normalcolor [\text{label }\theequation]}}
inlineEq_command = r'''
\makeatletter
\renewcommand*{\@eqnnum}{{\normalfont \normalcolor \fcolorbox{blue}{white}{\color{gray}{\theequation}}}}
\newcommand*{\inlineEq}[2][]{%
  \begingroup
    % Put \refstepcounter at the beginning, because
    % package `hyperref' sets the anchor here.
    \refstepcounter{equation}%
    \ifx\\#1\\%
    \else
      \label{#1}%
    \fi
    % prevent line breaks inside equation
    \relpenalty=10000 %
    \binoppenalty=10000 %
    \ensuremath{%
      % \displaystyle % larger fractions, ...
      #2%
    }%
    ~\@eqnnum
  \endgroup
} % cite: https://tex.stackexchange.com/a/78582
\makeatother
'''

cmark_command = r'''
\newcommand{\cmark}{
  \tikz[scale=0.23]{
    \draw[line width=0.7,line cap=round] (0.25,0) to [bend left=10] (1,1);
    \draw[line width=0.8,line cap=round] (0,0.35) to [bend right=1] (0.23,0);
  }
}
'''

xmark_command = r'''
\newcommand{\xmark}{
  \tikz[scale=0.23]{
    \draw[line width=0.7,line cap=round] (0,0) to [bend left=6] (1,1);
    \draw[line width=0.7,line cap=round] (0.2,0.95) to [bend right=3] (0.8,0.05);
  }
}
'''

QA_env = r'''
\newenvironment{QandA}{\begin{enumerate}\bfseries}{\end{enumerate}}
\newenvironment{answered}{\setlength{\parindent}{1em}\par\normalfont}{}
'''

def generateLatex(content, out_fp="output.tex", packages=[], commands=[]):
  eq_ct = 0
  framed = False

  output = [
    r'\documentclass[fleqn]{scrartcl}', #align everything with document class
    r'\usepackage{amsmath, tikz}',
    r'\usepackage{mathtools}',
    r'\usepackage{breqn}',
    r'\breqnsetup{compact,breakdepth={0},spread={4pt}}',
    r'\usepackage[normalem]{ulem}',
    r'\useunder{\uline}{\ulined}{}',
    r'\usepackage{float}',
    r'\usepackage{hyperref}',
    r'\hypersetup{colorlinks=true, linkcolor=blue}'
  ]

  for pkg in packages:
    if type(pkg) == dict:
      # e.g. format: {"breqn": {"breqnsetup": ["compact", ("breakdepth", 0), ("spread", "4pt")]}}
      # ==> \usepackage{breqn}
      #     \breqnsetup{compact,breakdepth={0},spread={4pt}}
      for pkg_name, pkg_setup in pkg.items():
        # assumes type(pkg_name) == str and type(pkg_setup) == dict
        output.append(r'\usepackage{' + str(pkg_name) + '}')
        if type(pkg_setup) == list:
          for spec in pkg_setup:
            output.append(spec)
        else:
          for param, specs in pkg_setup.items():
            setup_command = f'\\{param}{{' # => \the_param{
            # assumes type(param) == list and type(specs) == list
            for i, spec in enumerate(specs):
              # type(spec) can either be str or tuple (if value is assigned to spec as `spec={value}`)
              if type(spec) == str: setup_command += str(spec)
              else: setup_command += str(spec[0]) + '={' + str(spec[1]) + '}'
              if i < len(specs)-1: setup_command += ','
              else: setup_command += "}"
            output.append(setup_command)
    elif pkg[0] == '\\': output.append(pkg) #already formatted
    else: output.append(r'\usepackage{' + str(pkg) + '}')

  output.extend([
    r'\begin{document}',
    r'\newcommand{\header}[2][\ulined\bfseries\itshape]{{\Large #1{#2}} \\}',
    r'\newcommand{\Det}[1]{\begin{vmatrix} #1 \end{vmatrix}}',
    r'\def\eqq{\hiderel{=}}',
    r'\DeclareFlexCompoundSymbol{\coloneq}{Rel}{\mathrel{\vcenter{\hbox{:}}{=}}}',
    r'\renewcommand{\coloneqq}{\hiderel{\coloneq}}',
    r'\def\approxx{\hiderel{\approx}}',
     r'\def\conditionmath{\condition*}',
    r'\abovedisplayskip=3pt',
    r'\belowdisplayskip=3pt',
    r'\newcommand{\displaySkip}[2][]{ \\[#2]#1}',
    inlineEq_command,
    cmark_command,
    xmark_command,
    QA_env,
    r'\let\oldref\ref',
    r'\renewcommand{\ref}[1]{\textcolor{blue}{[}\oldref{#1}\textcolor{blue}{]}}'
    # r'\renewcommand{\ref}[1]{\textcolor{blue}{\uline{\oldref{#1}}}}'
  ])

  output.extend(commands) # for now 

  env = None
  dgroup = False

  for eq in content:
    formatted_eq = []

    if len(output) and (eq == Latex._newpage or (type(eq) == str and '\\begin{description}' in eq)) and output[-1][-2:] == r'\\': output[-1] = output[-1][:-2] #prevent latex error

    if isinstance(eq, Path): eq_type = "file" # path to some pre-formatted latex to insert
    elif Latex.isLatexCommand(eq): eq_type = "latex"
    elif "sympy" in str(type(eq)): eq_type = "sympy"
    elif type(eq) == tuple: eq_type = "sympy eq"
    elif type(eq) == list: eq_type = "sentence"
    elif callable(eq):
      if isinstance(content, sp.Poly):
        content = content.as_expr()
        eq_type = "sympy"
      else:
        eq()
        continue
    else: eq_type = str(type(eq))
    
    surround_with_curly = False
    if r"\conditionmath" in str(output[-1]).strip().split(' ')[-1]:
      surround_with_curly = True
      formatted_eq.append("{")

    if framed and str(output[-1]).strip().split(' ')[-1] != r'\quad' and r"\condition" not in str(output[-1]).strip().split(' ')[-1]:
      if env is not None:
        formatted_eq.append(r'\end{' + env + r'*}')
        # output.append(r'\end{' + env + r'*}')
        env = None
      formatted_eq.append(r'\end{dgroup*}')
      # output.append(r'\end{dgroup*}')
      dgroup = False
      framed = False

    if eq_type == "file":
      with open(eq, "r+") as f:
        tex = f.read().strip().strip("\n") # remove leading and trailing whitespaces/newlines
        tex = re.sub('%.+\n', '', tex) # remove comments
        if r"\begin{document}" in tex:
          if r"\begin{document}" in tex: tex = tex[tex.index(r"\begin{document}")+16:].strip().strip("\n") # 16 so get rid of entire r"\begin{document}"
          if r"\end{document}" in tex: tex = tex[:tex.index(r"\end{document}")].strip().strip("\n") # \begin{dmath

          if tex[:2] == "$$" or tex[:2] == r"\[": # continue prev math env
            tex = tex[2:]
            if not dgroup: formatted_eq.append(r"\begin{dgroup*}")
            # if not dgroup: output.append(r"\begin{dgroup*}")
            dgroup = True
            if env != "dmath":
              eq_ct += 1
              formatted_eq.append(r"\begin{dmath*}\label{eq:" + str(eq_ct) + "}")
            # if env != "dmath": output.append(r"\begin{dmath*}")
            env = "dmath"
            if tex[-2:] == "$$" or tex[-2:] == r"\]": tex = tex[:-2]
            # if tex[-2:] != "$$" and tex[-2:] != r"\]": env = "dmath" 
          else:
            if env == "dmath": formatted_eq.append(r"\end{dmath*}") #since we're going to either be in no env or start it again
            # if env == "dmath": output.append(r"\end{dmath*}") #since we're going to either be in no env or start it again
            env = None

            if tex[0:12] == r"\begin{dmath": #starting in math environment
              if not dgroup: formatted_eq.append(r"\begin{dgroup*}")
              # if not dgroup: output.append(r"\begin{dgroup*}")
              dgroup = True
              if not r"\end{dmath" in tex[-12:]: env = "dmath"

        formatted_eq.append(tex.strip().strip("\n"))
        # output.append(tex.strip().strip("\n"))
    elif "sympy" in eq_type:
      # if env != "dmath":
      if eq_type == "sympy eq" and eq[0] == Latex._eqframe:
        framed = True
        if env == "dmath":
          formatted_eq.append(r'\end{dmath*}')
          # output.append(r'\end{dmath*}')
          env = None

        if dgroup: formatted_eq.append(r'\end{dgroup*}')
        formatted_eq.append(r'\begin{dgroup*}' + Latex._eqframe)
        # if dgroup: output.append(r'\end{dgroup*}')
        # output.append(r'\begin{dgroup*}' + Latex._eqframe)
        dgroup = True
        eq = eq[1:]
      
      if not dgroup:
        formatted_eq.append(r'\begin{dgroup*}')
        # output.append(r'\begin{dgroup*}')
        dgroup = True
      
      # if not dgroup:
      #   if eq_type == "sympy eq" and eq[0] == Latex._eqframe:
      #     framed = True
      #     output.append(r'\begin{dgroup*}' + Latex._eqframe)
      #     dgroup = True
      #     eq = eq[1:]
      #   else:
      #     output.append(r'\begin{dgroup*}')
      #     dgroup = True
      
      if eq_type == "sympy":
        if env != "dmath":
          env = "dmath"
          eq_ct += 1
          formatted_eq.append(r'\begin{' + env + r'*}\label{eq:' + str(eq_ct) + '}')
      else:
        if env == "dmath" and eq[0] not in Latex.rel_symbols and str(output[-1]).strip().split(' ')[-1] != r'\quad' and r'\condition' not in str(output[-1]).strip().split(' ')[-1]:
          formatted_eq.append(r'\end{dmath*}')
          eq_ct += 1
          formatted_eq.append(r'\begin{dmath*}\label{eq:' + str(eq_ct) + "}")
          # formatted_eq.append(r'\begin{dmath*}')
        elif env != "dmath":
          env = "dmath"
          eq_ct += 1
          formatted_eq.append(r'\begin{' + env + r'*}\label{eq:' + str(eq_ct) + '}')
          # formatted_eq.append(r'\begin{' + env + r'*}')

      formatted_eq.append(formatEq(eq, env))
      # output.append(formatEq(eq, env))
    elif eq_type == "latex":
      if env is not None:
        if env == "dmath":
          formatted_eq.append(r'\end{' + env + r'*}')
          # output.append(r'\end{' + env + r'*}')
      if dgroup:
        formatted_eq.append(r'\end{dgroup*}')
        # output.append(r'\end{dgroup*}')
        dgroup = False
        env = None
      
      formatted_eq.append(str(eq))
      # output.append(str(eq))
    else:
      if env is not None:
        formatted_eq.append(r'\end{' + env + r'*}')
        # output.append(r'\end{' + env + r'*}')
      if dgroup:
        formatted_eq.append(r'\end{dgroup*}')
        # output.append(r'\end{dgroup*}')
        dgroup = False
      env = None
      
      if eq_type == "sentence":
        if not len(eq): continue
        if eq[-1] == Latex._newpage and output[-1][-2:] == r'\\': output[-1] = output[-1][:-2] #TODO: check
        sent = formatSentence(eq, env)
        if eq[-1] != Latex._quad and r"\condition" not in str(eq[-1]) and not Latex.isLatexCommand(eq[-1]): sent += r' \\'
        formatted_eq.append(sent)
      elif Latex.isMathSymbol(eq) and not r'\def' in str(eq): formatted_eq.append(r"$" + sp.latex(eq, order=Latex.sp_order) + r"$")
      elif r'\end{center}' in str(eq) or '\Large' in str(eq): formatted_eq.append(str(eq))
      else: formatted_eq.append(str(eq) + r' \\')

    if surround_with_curly: formatted_eq.append("}")
    
    formatted_eq = "\n".join(formatted_eq)
    if "%" in formatted_eq and formatted_eq[-2:] == r'\\':
      formatted_eq = formatted_eq.split("%")
      formatted_eq = formatted_eq[0] + r'\\ %' + formatted_eq[1][:-2]

    output.append(formatted_eq)

    Latex.reset_eval()
  if env == "dmath": output.append(r'\end{' + env + r'*}')

  output.append(r'\end{document}')

  with open(out_fp, "w+") as f:
    f.writelines("\n".join(output))
