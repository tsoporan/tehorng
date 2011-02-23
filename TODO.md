tehorng todo
============

Just some ideas of what should be added/fixed to tehorng (in no particular order)

- __internalization/localization__, basically make all of tehorng localized per user, perhaps allow more language options (long-term)
- a way to __track user "Activity"__, model object that stores actions along with timestamps, using signals framework (actions: adding, editing, reporting)
- __reputation system__, actions should award reputation, users can use reputationa as currency, reputation unlocks different privileges (adding stuff, likes, editing, filling requests grants reputation)
- __global editing/adding information__, allow all users to modify and create content, a reversion-like system is in place
- user messaging swapped out for django-pm 
- refactor code into distinct and clear apps/places (long-term)
- new layout (long-term, needs to be more usable)
- improve search
- write tests (needed badly =/)
- a robust automated link checking solution (perhaps only allow certain services, but do them well)
- __rid of email email verification__ in favor of reCaptcha
- add documentation/guides/instructions, generally just more verbosity in terms of what things are and do (needed badly)
- __Request__ functionality
- don't actually delete anything, just remove it from visibility
- migrate to PostgreSQL
