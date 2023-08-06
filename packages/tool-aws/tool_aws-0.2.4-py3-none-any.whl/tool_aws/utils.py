from pyproj import Proj, transform


def reprojectBBox(bbox, sridTo, sridFrom=2056):
    if sridTo == sridFrom:
        return bbox
    sridIn = Proj('EPSG:%s' % sridFrom)
    sridOut = Proj('EPSG:%s' % sridTo)
    pLeft = transform(sridIn, sridOut, bbox[0], bbox[1])
    pRight = transform(sridIn, sridOut, bbox[2], bbox[3])
    return pLeft + pRight
