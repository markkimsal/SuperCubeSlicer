import sys
import cubeslicer.model
import cubeslicer.geom
from cubeslicer.model import Model2d

def process(model, pipeline):

	print "finding polylines"
	for layid in model.layers:
		line1idx=0
		lay = model.layers[layid]
		for line1 in lay.lines:
			line1idx = line1idx+1

			a1 = ( line1.a().X, line1.a().Y )
			b1 = ( line1.b().X, line1.b().Y )
			match = False

			for line2 in lay.lines:
				if line1 == line2:
					continue

				a2 = ( line2.a().X, line2.a().Y )
				b2 = ( line2.b().X, line2.b().Y )

				a1 = ( round(a1[0], 4), round(a1[1], 4))
				b1 = ( round(b1[0], 4), round(b1[1], 4))

				a2 = ( round(a2[0], 4), round(a2[1], 4))
				b2 = ( round(b2[0], 4), round(b2[1], 4))

				#end meets beginning
				if a1 == b2 \
					or b1 == a2:
						polyline = cubeslicer.geom.PolyLine( line1, line2 )
						print line1, polyline
						lineidx = lay.lines.index(line1)
						lay.lines.remove(line1)
						lay.lines.remove(line2)
						lay.lines.insert(lineidx, polyline)
						line1 = polyline
						continue

				#end meets beginning
				if a2 == b1 \
					or b2 == a1:
						polyline = cubeslicer.geom.PolyLine( line2, line1 )
						print line1, polyline
						lineidx = lay.lines.index(line1)
						lay.lines.remove(line1)
						lay.lines.remove(line2)
						lay.lines.insert(lineidx, polyline)
						line1 = polyline
						continue

				# beginning meets beginning
				if a1 == a2:
						polyline = cubeslicer.geom.PolyLine( line1, line2 )
						print line1, polyline
						lineidx = lay.lines.index(line1)
						lay.lines.remove(line1)
						lay.lines.remove(line2)
						lay.lines.insert(lineidx, polyline)
						line1 = polyline
						continue

				# end meets end
				if b1 == b2:
						polyline = cubeslicer.geom.PolyLine( line1, line2 )
						print line1, polyline
						lineidx = lay.lines.index(line1)
						lay.lines.remove(line1)
						lay.lines.remove(line2)
						lay.lines.insert(lineidx, polyline)
						line1 = polyline
						continue

