class PackModel {
  final String title;
  final int length;
  final int? progress;
  final List<String> urls;
  PackModel({
    required this.title,
    required this.length,
    this.progress,
    required this.urls,
  });
}
