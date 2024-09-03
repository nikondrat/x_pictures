import 'dart:ui'; // Required for ImageFilter

import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:x_pictures/src/data.dart'; // Import CachedNetworkImage package

class EnhanceBody extends StatefulWidget {
  final PackModel model;
  const EnhanceBody({super.key, required this.model});

  @override
  State<EnhanceBody> createState() => _EnhanceBodyState();
}

class _EnhanceBodyState extends State<EnhanceBody> {
  double _linePosition = 0.5;

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return ClipRRect(
      borderRadius: BorderRadius.circular(AppValues.kRadius),
      child: Stack(
        children: [
          widget.model.images.isNotEmpty
              ? CachedNetworkImage(
                  imageUrl: widget.model.images[0].url,
                  fit: BoxFit.cover,
                  width: double.infinity,
                  height: double.infinity,
                )
              : const Center(
                  child: Icon(Icons.image_not_supported_outlined),
                ),
          Column(
            children: [
              Expanded(
                child: GestureDetector(
                  onHorizontalDragUpdate: (details) {
                    setState(() {
                      _linePosition += details.primaryDelta! /
                          MediaQuery.of(context).size.width;
                      _linePosition = _linePosition.clamp(0.0, 1.0);
                    });
                  },
                  child: Stack(
                    children: [
                      Positioned.fill(
                        child: FractionallySizedBox(
                          widthFactor: _linePosition,
                          alignment: Alignment.centerLeft,
                          child: ClipRect(
                            child: BackdropFilter(
                              filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                              child: Container(
                                color: Colors.black.withOpacity(0),
                              ),
                            ),
                          ),
                        ),
                      ),
                      Positioned(
                        left:
                            MediaQuery.of(context).size.width * _linePosition -
                                2,
                        top: 0,
                        bottom: 0,
                        child: Container(
                          width: 8,
                          color: colorScheme.primary,
                        ),
                      ),
                      Positioned(
                        left:
                            MediaQuery.of(context).size.width * _linePosition -
                                23,
                        top: (MediaQuery.of(context).size.height * 0.4),
                        child: GestureDetector(
                          onPanUpdate: (details) {
                            setState(() {
                              _linePosition += details.delta.dx /
                                  MediaQuery.of(context).size.width;
                              _linePosition = _linePosition.clamp(0.0, 1.0);
                            });
                          },
                          child: Container(
                            width: 50,
                            height: 50,
                            decoration: BoxDecoration(
                              color: colorScheme.primary,
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(
                              Icons.code,
                              size: 24,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
          Positioned(
            left: 20.0,
            top: 10.0,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.5),
                borderRadius: BorderRadius.circular(4),
              ),
              child:
                  AutoSizeText(t.toolsView.before, style: textTheme.bodyLarge),
            ),
          ),
          Positioned(
            right: 20.0,
            top: 10.0,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.5),
                borderRadius: BorderRadius.circular(4),
              ),
              child:
                  AutoSizeText(t.toolsView.after, style: textTheme.bodyLarge),
            ),
          ),
        ],
      ),
    );
  }
}
