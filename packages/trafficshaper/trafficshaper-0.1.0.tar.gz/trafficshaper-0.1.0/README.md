# Intro

Tired of dealing with major & minor numbers? You like the TOML format (kind of "ini" on steroids)?
Always wanted to play with traffic shaping on linux but it turned too complex or confusing?
This alpha tool aims at simplifying the learning curve for traffic control on ip route 2.

The format started quite close to the original command-line and progressively adds more support and shorter or easier notations.

Forget about `classid`, `flowid`.
Consider `parent` sometimes handle for `complex` scenarios only!

Check the *examples* folder to dive into the syntax.

# Supported features

- hosts aliases
- network interfaces aliases
- speeds aliases
- automatic generation of major & minor mumbers (all of them!) when possible
- visual representation of the setup

## Trafic control coverage

- sfq : makes a more fair traffic
- netem : simulate network problems
- htb : control traffic rate using categories
- tbf : very basic shaping

## TODO:

- relative speeds (percents)
- templates (for repeated attributes)

## QDiscs

- sfq
- netem
- htb
- tbf

## Classes (categories uses by some QDiscs)

- htb

## Filters (assign traffic)

- fw
- u32
  - ip (src, dst, sport, dport)
- action

