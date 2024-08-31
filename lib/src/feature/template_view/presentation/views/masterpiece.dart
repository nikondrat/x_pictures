import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class MasterpieceView extends StatefulWidget {
  final LoraModel model;
  const MasterpieceView({super.key, required this.model});

  @override
  State<MasterpieceView> createState() => _MasterpieceViewState();
}

class _MasterpieceViewState extends State<MasterpieceView> {
  @override
  Widget build(BuildContext context) {
    return Provider(
      create: (context) => PhotosLoaderStore(
        model: widget.model,
      ),
      builder: (context, child) {
        final store = Provider.of<PhotosLoaderStore>(context);
        return MasterpieceBody(store: store);
      },
    );
  }
}
