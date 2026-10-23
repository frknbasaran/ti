---
title: Rebuilding the Kadıköy ferry pier as it was in 2008
description: How the Kadıköy ferry pier grew from a 38-metre placeholder to the real building, measured from photos, with rooms behind its windows and 26 years of weather.
date: 2026-10-20
game: project-r
heroImage: ../../../assets/project-r/pier_aged_front.jpg
heroImageAlt: The land front of the Kadıköy ferry pier in Project R at dusk, with the sign KARAKÖY EMİNÖNÜ İSKELESİ, two red LED departure boards, rain streaks under the cornice and a Turkish flag on a pole.
draft: true
---

Hi,

Project R is set on the Kadıköy quay in Istanbul, in February 2008. The building you see more than any other in the game is the ferry pier, the Karaköy–Eminönü pier, right on the quay. Ferries come and go from its sides all day, and the crowds walk in and out through its doors. If it looks wrong, everything around it looks wrong too.

## A placeholder three times too small

The first pier in the game was 38 metres long. The real one is 98.5 metres long. It opened in 1982, so in 2008 it was 26 years old.

I didn't have drawings, so the measurements came from three places. OpenStreetMap gave the outline and the lengths of the sides. A photo from 2009, taken almost straight at the long side, gave the heights once I scaled it to the map's length. And I checked one against the other: the gap between the deck and the water in the photo came out at 1.9 metres, against 1.8 in the records.

Going to the real size moved a lot more than the building. Every ferry berth, every path the crowd walks, every door and collider, the menu camera and the navigation mesh had to move with it.

The photos also had to be read with care, because the pier has changed since 2008. Today there are café umbrellas, glass railings and a newer fence with a logo on it. None of that was there in 2008, so none of it is in the game.

## The front you walk into

The land front is what you see from the quay: two big arches under the sign KARAKÖY EMİNÖNÜ İSKELESİ. In the first versions it was flat. Two blank panels, three plain piers and bright glass screens just behind the arches.

The 2009 photo shows a lot more once you look at it at full size, and I measured it rather than guessing. Pixel profiles across the wall gave the pattern:

- The panels are covered in fine horizontal ribs, about 7 cm apart.
- Only the middle pier is ribbed. The two corner piers are smooth plaster with a horizontal joint every 30 cm, and every second joint is deeper than the one between. The joints turn the corner and carry on along the side.
- The wall between the arches and the sign is ribbed vertically.
- The cornice steps forward over each pier.

![The land front of the Kadıköy pier as an untextured model: two arches, the KARAKÖY EMİNÖNÜ İSKELESİ sign, ribbed panels above, and corner piers with horizontal joints.](../../../assets/project-r/pier_land_front_blender.jpg)

The ribs and joints are textures, not geometry. Modelling a 6 cm rib costs almost nothing in triangles, but from 30 metres away a rib is smaller than a pixel, and things smaller than a pixel shimmer as you move. A texture fades smoothly into a soft grey tone as you walk away, which is also what the real wall does in the photo. I drew the joints a little wider and darker than the real 1.5 cm, because at the real width they disappear entirely from the quay.

Behind the arches, the bright screens are gone. Now there's a deep, dim hall about six metres long, with the glass doors at the far end, and people walk into the dark the way they did in 2008.

## Windows with rooms behind them

The long sides of the pier are what you see most from the quay. In the old model the pointed windows were just hollows cut into a flat wall, their glass a flat glowing colour, and nothing behind them.

I took three photos of my own of the wing: the whole side at an angle, three bays, and a single bay close up. My first measurements came from the close-up, and they were wrong. The photo was taken at an angle, which squeezes widths, so the windows came out narrow and the big arch came out round like a vault. Measuring the widths from a front-on photo from 2019 and correcting for the angle fixed it. The top of the big arch turned out to be neither pointed nor round: round shoulders, then a flat 22-degree tent at the very top, so it got its own curve.

![One bay of the pier's wing as an untextured model: two pointed windows with lattice heads above, two rectangular windows below, panelled pilasters and ribbed arch faces.](../../../assets/project-r/pier_wing_bay_blender.jpg)

Behind the glass there are real rooms now. On the wing, a waiting hall below and offices above, with desks, CRT monitors and cabinets. In the pavilion at the end, a café upstairs and a waiting hall with a ticket counter below. My first try lit them in light colours, and by day the windows read as bright grey walls. From outside a real room looks dark in daylight, so the rooms now get only about a tenth of the sky's light. By day the glass is dark and reflects the sky, and you can just make out the furniture. At night each office is lit its own way: fluorescent tubes, a single desk lamp, or nothing at all. A few tubes are dead.

Each pane of glass takes a different quarter of a dirt texture, so no two neighbours look the same. They're dirtier at the bottom and in the corners, with rain marks from above, and they have the slight wave of old glass.

## The tyres along the edge

Along the side where the ferries berth, the real pier has a row of old truck tyres hung on wires, so the ferries lean on rubber and not on concrete. The first ones in the game were eight-sided rings with a square section. From the quay they looked like toys.

Now there are 105 of them, close to touching, the way they hang in photos of the pier. Each one is built from a single profile, with bead, bulging sidewall, round shoulder and tread, and the textures are made from that same profile. Because the texture knows which part of the tyre hangs at the top and which part sits in the sea, the tops are dusty and salty and the bottoms are wet and green. There are three wear variants, and every tyre hangs at a slightly different tilt and height. Each one hangs from two thin galvanised wires.

![The tyres on the pier's edge before and after: on the left, grey eight-sided rings; on the right, black truck tyres with deep treads hanging on thin wires above the water.](../../../assets/project-r/pier_tyres_before_after.jpg)

## Twenty-six years of weather

A 26-year-old building on the sea doesn't look freshly painted, and the pier did. The hard part was that about 90% of the cream front had no texture coordinates, so I couldn't simply paint dirt onto it.

The first step works without them. The game's surface shader ages a material in world space: rain streaks hanging from the cornice, chalky faded paint, dust on ledges, soot under the eaves, rust on steel. That got the overall feel, but world space doesn't know where the window sills or the sign band are, so streaks could only hang from the roofline.

So the building got its own wear map as well. I gave its outside a second set of texture coordinates, then measured every texel of it: where it is, which way it faces, what material it's on, and how much sky it can see, with three rays cast upwards from every wall texel and ambient occlusion baked in Blender. From that a script paints a 4096 × 4096 map: real streaks under every sill, arch and sign band, soot in the recesses, a damp and salt line at the foot of the walls, stains in the cream paint and dirt in the corners. It covers the visible walls at about one texel every 2.4 cm.

## Optimization

The whole pier is about 133,000 triangles. That sounds like a lot for one building, so I counted where they go.

About 93,000 of them, 70%, are the tyres. The building itself, with its bays, rooms, railings and sign, is about 40,000. The tyres already get simpler with distance: the ones more than 40 metres from the quay have fewer segments, which brought them down from about 104,000. But a thousand triangles a tyre is still a lot for something you see from at least a few metres away, and it's the same three tyres over and over.

Unlike a building on the far shore, you can get close to some of these tyres and far from others, so this is a case where levels of detail make sense. The option I'm keeping in the backlog is to bake the detailed tyre's shape into a normal map, use a much lighter tyre for everything but the nearest few, and draw the three variants as instances. I'd expect most of those 93,000 triangles to go without a visible change, but I won't know the real number until I've done it.

## The numbers

- 98.5 m long, up from the 38 m placeholder
- Ribs about 7 cm apart, corner joints every 30 cm
- 105 tyres, three wear variants
- 42 room lights, each office lit its own way
- Wear map 4096 × 4096, one texel about every 2.4 cm
- About 133,000 triangles, 93,000 of them in the tyres

If you remember this pier from 2008 and something here doesn't match, I'd love to hear about it.

*Map data © OpenStreetMap contributors, ODbL.*
