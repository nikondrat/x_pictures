import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class MasterpieceView extends StatefulWidget {
  final PacksStore store;
  final LoraModel model;
  const MasterpieceView({super.key, required this.store, required this.model});

  @override
  State<MasterpieceView> createState() => _MasterpieceViewState();
}

class _MasterpieceViewState extends State<MasterpieceView> {
  @override
  Widget build(BuildContext context) {
    return Provider(
      create: (context) => PhotosLoaderStore(
        store: widget.store,
        model: widget.model,
      ),
      builder: (context, child) {
        final store = Provider.of<PhotosLoaderStore>(context);
        return MasterpieceBody(store: store);
      },
    );
  }
}
