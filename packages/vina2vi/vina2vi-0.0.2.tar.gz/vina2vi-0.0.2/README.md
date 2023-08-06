# vina2vi
`vina2vi` stands for _**Vi**etnamese **n**o **a**ccent **to** **Vi**etnamese_,  
which is a Python package aiming at helping foreigners **decrypt** messages
in Vietnamese. (More precisely,
foreigners who already know the basics of the language.)

Among other things, this Python package tries to
- Restore from Vietnamese w/o diacrytics to w/ diacrytics
- Translate acronyms, **teencode**, etc.


## Installation
Run the following to install:

```python
pip install vina2vi
```


## Usage
I only work on this project on spare time, and work slowly. So this README
will get changed a lot in the future. For the moment, there is not much in
the package that is super useful. As time goes by, I will add more.

```python
In [1]: from vina2vi.utils import Vietnamese

In [2]: Vietnamese.is_foreign("Российская Федерация\tRossiyskaya Federatsiya")
Out[2]: True

In [3]: Vietnamese.is_foreign("\n\tRossiyskaya Federatsiya")
Out[3]: False

In [4]: Vietnamese.is_foreign("Tôi nói tiếng Việt Nam\t碎呐㗂越南")
Out[4]: True

In [5]: Vietnamese.is_foreign("Tôi nói tiếng Việt Nam\t")
Out[5]: False
```


