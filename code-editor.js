// Defining rectangle (Iron Gate Reservoir and Copco Reservoir)
var geometry = ee.Geometry.Polygon([
  [
    [-122.47010097089289, 41.92072985609173],
    [-122.26067409101007, 41.92072985609173],
    [-122.26067409101007, 41.99987210809549],
    [-122.47010097089289, 41.99987210809549],
    [-122.47010097089289, 41.92072985609173],
  ],
]);
var roi = geometry;
var targetDate = '2019-09-10'; // Data for sentinel-2 image

// Date range
var startDate = ee.Date(targetDate).advance(-1, 'day');
var endDate = ee.Date(targetDate).advance(1, 'day');

var sentinel2Collection = ee.ImageCollection('COPERNICUS/S2')
  .filterBounds(roi)
  .filterDate(startDate, endDate)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)); 
var bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7','B8', 'B8A']; // Bands B1 to B8A

// Create a function to mask clouds using the QA60 band
function maskClouds(image) {
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  var qa60 = image.select(['QA60']);
  var cloudMask = qa60.bitwiseAnd(cloudBitMask).eq(0)
    .and(qa60.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(cloudMask).select(bands);
}
var sentinel2Composite = sentinel2Collection.map(maskClouds);
//for visualization
var trueColor = {
  bands: ['B4', 'B3', 'B2'],
  min: 0,
  max: 3000
};
// Display the Sentinel-2 imagery on the map
Map.centerObject(roi, 12);
Map.addLayer(sentinel2Composite.median(), trueColor, 'Sentinel-2 True Color');
// Export the composite to Google Drive
var exportOptions = {
  region: roi,
  scale: 10,
  fileFormat: 'GeoTIFF',
  formatOptions: {
    cloudOptimized: true
  }
};

//exporting the images to drive
Export.image.toDrive({
  image: sentinel2Composite.median(),
  description: 'Sentinel2_Composite_' + targetDate,
  folder: 'AlgalBloom_SentinalData', 
  region: roi,
  scale: 10, 
  maxPixels: 1e13,
});
