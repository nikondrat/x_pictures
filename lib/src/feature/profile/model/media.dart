enum MediaType {
  image,
  video,
}

class MediaModel {
  final MediaType type;
  final String url;

  final DateTime createdDate;

  MediaModel(
      {required this.type, required this.url, required this.createdDate});
}
