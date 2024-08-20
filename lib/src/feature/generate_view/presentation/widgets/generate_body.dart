import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class GenerateBody extends StatefulWidget {
  final GenerateStore store;
  final double windowHeight;
  final double windowWidth;
  const GenerateBody(
      {super.key,
      required this.store,
      required this.windowWidth,
      required this.windowHeight});

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
    final MediaQueryData mediaQueryData = MediaQuery.of(context);

    return LoadingWidget(
      future: widget.store.data,
      builder: (v) => ListView(
        padding: HorizontalSpacing.centered(widget.windowWidth),
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
                useSafeArea: true,
                shape: const BeveledRectangleBorder(
                    borderRadius: BorderRadius.vertical(
                        top: Radius.circular(AppValues.kRadius))),
                builder: (context) {
                  return Padding(
                    padding: EdgeInsets.fromLTRB(
                        20.h, 20.h, 20.h, mediaQueryData.viewInsets.bottom),
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
          Gap(AppValues.kPadding.h),
        ],
      ),
    );
  }
}
