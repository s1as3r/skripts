# Aniname

Get names of anime episodes and also check if an episode if filler or not.
I know there are a lot of things that could be done in a better way (argument parsing etc)
but i'm just too lazy.

## Usage

- Run `python3 aniname.py <anime_name>` to get the names, filler guide for all the episodes of `anime_name`.
  - e.g, `python3 aniname.py "Naruto Shippuden"` will get all the episode names of naruto shippuden.
- Run `python3 aniname.py <anime_name> -e EPS` to get the names, filler guide for `EPS`. Here `EPS` can be multiple numbers or/and a range of episodes
  - e.g, `python3 aniname.py "Naruto Shippuden" -e 1 2 5-7` will get the episode names of naruto shippuden episodes 1, 2, 5, 6 and 7.
- You can also save the episode names of an anime by running `python3 aniname.py <anime_name> -s`
