import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/data.dart';

class OfficePage extends StatelessWidget {
  const OfficePage({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final ColorScheme colorScheme = themeData.colorScheme;

    return Scaffold(
      appBar: const CustomAppBar(textName: 'Office'),
      floatingActionButton: CustomFloatingButton(
        buttonName: 'Get this pack',
        onTap: () {
          router.goNamed(AppViews.disclaimarPageRoute);
        },
      ),
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            pinned: true,
            expandedHeight: 200.h,
            backgroundColor: colorScheme.surface,
            leading: const SizedBox(),
            flexibleSpace: const FlexibleSpaceBar(
              background: ImageItemOffice(),
            ),
            bottom: PreferredSize(
              preferredSize: Size.fromHeight(0.h),
              child: Container(
                width: double.infinity,
                decoration: BoxDecoration(
                  color: colorScheme.surface,
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(20.r),
                    topRight: Radius.circular(20.r),
                  ),
                ),
                child: const Text(''),
              ),
            ),
          ),
          const SliverToBoxAdapter(child: OfficePageBody()),
          SliverPadding(
            padding: EdgeInsets.only(
              left: 15.w,
              right: 15.w,
              bottom: 90.w,
            ),
            sliver: const SliverGridView(),
          ),
        ],
      ),
    );
  }
}
