import sys
import vlicer.model
import vlicer.geom
from vlicer.model import Model2d

def process(model, pipeline):

	reducedLines = 0
	firstLoop = True
	while reducedLines or firstLoop:
		if not firstLoop:
			print "lines reduced ", reducedLines
		firstLoop = False
		reducedLines = 0
		for layid in model.layers:
			line1idx=0
			lay = model.layers[layid]
			for line1 in lay.lines:
				line1idx = line1idx+1
				#if line1idx == 1:
				#	continue
				a1 = ( line1.a().X, line1.a().Y )
				b1 = ( line1.b().X, line1.b().Y )
				match = False

				for line2 in lay.lines:
					if line1 == line2:
						continue
					#for line2 in lay.lines:

					a2 = ( line2.a().X, line2.a().Y )
					b2 = ( line2.b().X, line2.b().Y )

					a1 = ( round(a1[0], 4), round(a1[1], 4))
					a2 = ( round(a2[0], 4), round(a2[1], 4))

					b1 = ( round(b1[0], 4), round(b1[1], 4))
					b2 = ( round(b2[0], 4), round(b2[1], 4))

					#if a2x and b1y and b1x == a2x and b1y == a2y and \
					#print a2x, b1y
					#end meets beginning
					if b1 == a2 :
						try:
							m1 = (a1[1] - b1[1]) / (a1[0] - b1[0])
						except ZeroDivisionError:
							m1 = None
						try:
							m2 = (a2[1] - b2[1]) / (a2[0] - b2[0])
						except ZeroDivisionError:
							m2 = None

						if (m1 == m2):
							#print " ", line1idx, b1x, a2x, b1y, a2y, m1, m2
							lay.lines.remove(line2)
							reducedLines = reducedLines+1
							line1.points['B'].X = b2[0]
							line1.points['B'].Y = b2[1]
							b1 = (line1.b().X, line1.b().Y)
							continue

							#lay.lines.insert( lay.lines.index(line1), line1)
							#print "slope match ", line1idx, a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y
							#continue
		
					#beginning meets end
					if a1 == b2:
						try:
							m1 = (a1[1] - b1[1]) / (a1[0] - b1[0])
						except ZeroDivisionError:
							m1 = None
						try:
							m2 = (a2[1] - b2[1]) / (a2[0] - b2[0])
						except ZeroDivisionError:
							m2 = None
						if (m1 == m2):
							lay.lines.remove(line2)
							reducedLines = reducedLines+1
							line1.points['A'].X = a2[0]
							line1.points['A'].Y = a2[1]
							a1 = (line1.a().X, line1.a().Y)
							continue

							#lay.lines.insert( lay.lines.index(line1), line1)
							#print "slope match ", line1idx, a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y
							#continue

					#beginning meets beginning
					if a1 == a2:
						try:
							m1 = (a1[1] - b1[1]) / (a1[0] - b1[0])
						except ZeroDivisionError:
							m1 = None
						try:
							m2 = (a2[1] - b2[1]) / (a2[0] - b2[0])
						except ZeroDivisionError:
							m2 = None
						if (m1 == m2):
							lay.lines.remove(line2)
							reducedLines = reducedLines+1
							line1.points['A'].X = b2[0]
							line1.points['A'].Y = b2[1]
							a1 = (line1.a().X, line1.a().Y)
							continue

							#lay.lines.insert( lay.lines.index(line1), line1)
							#print "slope match ", line1idx, a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y
							#continue

					#end meets end
					if b1 == b2:
						try:
							m1 = (a1[1] - b1[1]) / (a1[0] - b1[0])
						except ZeroDivisionError:
							m1 = None
						try:
							m2 = (a2[1] - b2[1]) / (a2[0] - b2[0])
						except ZeroDivisionError:
							m2 = None
						if (m1 == m2):
							lay.lines.remove(line2)
							reducedLines = reducedLines+1
							line1.points['B'].X = a2[0]
							line1.points['B'].Y = a2[1]
							b1 = (line1.b().X, line1.b().Y)
							continue

							#lay.lines.insert( lay.lines.index(line1), line1)
							#print "slope match ", line1idx, a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y
							#continue
