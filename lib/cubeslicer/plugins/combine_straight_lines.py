import sys, logging
import cubeslicer.model
import cubeslicer.geom
from cubeslicer.model import Model2d

def process_layer(model, lay, pipeline):

	smudge = 0.001
	reducedLines = 0
	firstLoop = True
	logging.info("lines before reduction %d", len(lay.lines))
	while reducedLines or firstLoop:
		if not firstLoop:
			logging.info( "lines reduced %d", reducedLines)
		firstLoop = False
		reducedLines = 0
		line1idx = 0
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

				if (a1 != a2) and (a1 != b2) and (b1 != a2) and (b1 != b2):
					continue
				#	logging.debug( "no line match %s, %s, %s, %s", a1, b1, a2, b2)


				prec = 4
				try:
					m1 = float('%.4f'%abs(( round(a1[1],prec) - round(b1[1],prec)) / ( round(a1[0],prec) - round(b1[0],prec) )))
				except ZeroDivisionError:
					m1 = None
				try:
					m2 = float('%.4f'%abs((round(a2[1],prec) - round(b2[1],prec)) / (round(a2[0],prec) - round(b2[0],prec))))
				except ZeroDivisionError:
					m2 = None

				#print m1, m2

				if b1 == a2 :
					if (m1 == m2):
						#print " ", line1idx, b1x, a2x, b1y, a2y, m1, m2
						lay.lines.remove(line2)
						reducedLines = reducedLines+1
						line1.b().X = line2.b().X
						line1.b().Y = line2.b().Y
						b1 = (line1.b().X, line1.b().Y)
						continue

						#lay.lines.insert( lay.lines.index(line1), line1)
						#print "slope match ", line1idx, a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y
						#continue
	
				#beginning meets end
				if a1 == b2:
					"""
					try:
						m1 = float('%.1f'%abs((a1[1] - b1[1]) / (a1[0] - b1[0])))
					except ZeroDivisionError:
						m1 = None
					try:
						m2 = float('%.1f'%abs((a2[1] - b2[1]) / (a2[0] - b2[0])))
					except ZeroDivisionError:
						m2 = None

					print m1, m2
					"""
					if (m1 == m2):
						lay.lines.remove(line2)
						reducedLines = reducedLines+1
						line1.a().X = line2.a().X
						line1.a().Y = line2.a().Y
						a1 = (line1.a().X, line1.a().Y)
						continue

						#lay.lines.insert( lay.lines.index(line1), line1)
						#print "slope match ", line1idx, a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y
						#continue

				#beginning meets beginning
				if a1 == a2:
					"""
					try:
						m1 = float('%.1f'%abs((a1[1] - b1[1]) / (a1[0] - b1[0])))
					except ZeroDivisionError:
						m1 = None
					try:
						m2 = float('%.1f'%abs((a2[1] - b2[1]) / (a2[0] - b2[0])))
					except ZeroDivisionError:
						m2 = None

					print m1, m2
					"""
					if (m1 == m2):
						lay.lines.remove(line2)
						reducedLines = reducedLines+1
						line1.a().X = b2[0]
						line1.a().Y = b2[1]
						a1 = (line1.a().X, line1.a().Y)
						continue

						#lay.lines.insert( lay.lines.index(line1), line1)
						#print "slope match ", line1idx, a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y
						#continue

				#end meets end
				if b1 == b2:
					"""
					try:
						m1 = float('%.1f'%abs((a1[1] - b1[1]) / (a1[0] - b1[0])))
					except ZeroDivisionError:
						m1 = None
					try:
						m2 = float('%.1f'%abs((a2[1] - b2[1]) / (a2[0] - b2[0])))
					except ZeroDivisionError:
						m2 = None

					print m1, m2
					"""
					if (m1 == m2):
						lay.lines.remove(line2)
						reducedLines = reducedLines+1
						line1.b().X = a2[0]
						line1.b().Y = a2[1]
						b1 = (line1.b().X, line1.b().Y)
						continue

						#lay.lines.insert( lay.lines.index(line1), line1)
						#print "slope match ", line1idx, a1x, a1y, b1x, b1y, a2x, a2y, b2x, b2y
						#continue
	logging.info("lines after reduction %d", len(lay.lines))
