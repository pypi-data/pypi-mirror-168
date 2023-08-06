# Sparragon
Simple automation interface for Galaxy Life
## Installation
This project is available on [PyPI](https://pypi.org/project/sparragon/) and can be installed with pip
```
pip install sparragon
```
or directly from github
```
pip install git+https://github.com/matcool/sparragon.git
```
## Usage
```python
import sparragon

r: Ressources = sparragon.Ressources()
r.get_gold_from_screen() # Will attempt to get how much gold you have from the top of your screen
print(r) # Prints out how much gold you have
```

### Todo
- [ ] Documentation
- [ ] More Tests
- [ ] More game-oriented functions
  - [ ] Wait for loading screen
  - [ ] Close prompts
- [ ] UI handling
  - [ ] Research lab UI
  - [ ] Training camp UI
  - [ ] Warp Gate UI
  - [ ] Bunker UI
  - [x] Upgrade UI
  - [ ] Build UI
  - [ ] Inventory/Crafting UI
  - [ ] Alliance UI