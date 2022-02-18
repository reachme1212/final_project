select c.index, c.county, c.labor_force, c.employed, c.unemployed, c.unemployed_pct, g.geoid
into county_geoid
from county_labor as c
right join "geoID" as g
on c.index = g.index

