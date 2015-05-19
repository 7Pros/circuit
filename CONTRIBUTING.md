# circuit

* git branch structure:
  * master
  * development
  * development_**featureName**

* git rules: 
  - master **untouchable**, only the project leader has access.
  - everyone develop in **their own branch** (development_**featureName**) and *after* it's been tested, comes into the **development branch**.
  - never merge master with your branch; IT MUST BE ALWAYS MERGED YOUR BRANCH WITH MASTER, BE CAREFUL!
    * EXAMPLE OF THE **CORRECT** WAY:
      * git branch
        * *master
        * development
        * development_juan
      * git checkout development_juan
      * git status
        * On branch development_juan
        * Your branch is up-to-date with 'origin/development'.
        * nothing to commit, working directory clean.
      * git merge master
    * EXAMPLE OF THE **WRONG** WAY:
      * git branch
        * *master
        * development
        * development_juan
      * git merge development_juan
    
    - All this is to preserve the stable version. The presented way to merge, it's possible and it should be done that way because     so you will always work with the latest stable version.
    
* git tips: 
  - Don't w8 to long to commit! Mixed commits with more than one stories or epics are harder to handle with in case of a bug. 
  - If your pushing into the development branch, don't forget to pull the latest version from the repository's branch.
    
    
