import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class GenerateBody extends StatefulWidget {
  final GenerateStore store;
  final double windowHeight;
  const GenerateBody(
      {super.key, required this.store, required this.windowHeight});

  @override
  State<GenerateBody> createState() => _GenerateBodyState();
}

class _GenerateBodyState extends State<GenerateBody> {
  @override
  void initState() {
    widget.store.fetchFilter();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final GenerateViewStore store = context.read<GenerateViewStore>();
    final GenerateStore genStore = context.read<GenerateStore>();

    return Column(
      children: [
        const Gap(AppValues.kPadding),
        const SelectModeWidget(),
        const Gap(AppValues.kPadding),
        const GenerateStyles(),
        const Gap(AppValues.kPadding),
        const GenerateTags(),
        const Gap(AppValues.kPadding),
        GenerateFormats(
          windowHeight: widget.windowHeight,
        ),
        const Gap(AppValues.kPadding),
        GestureDetector(
          onTap: () {
            showModalBottomSheet(
              context: context,
              shape: const BeveledRectangleBorder(
                  borderRadius: BorderRadius.vertical(
                      top: Radius.circular(AppValues.kRadius))),
              builder: (context) {
                return Padding(
                  padding: const EdgeInsets.all(AppValues.kPadding),
                  child: AddDescription(
                    store: store,
                    genStore: genStore,
                  ),
                );
              },
            );
          },
          child: AbsorbPointer(
              child: AddDescription(
            store: store,
            genStore: genStore,
          )),
        ),
        const Gap(AppValues.kPadding),
      ],
    );
  }
}
